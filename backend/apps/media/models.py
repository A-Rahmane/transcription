from django.db import models
from django.conf import settings

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_folders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True, related_name='files')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveBigIntegerField(help_text="Size in bytes")

    def save(self, *args, **kwargs):
        if self.file:
            self.size = self.file.size
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Permission(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='folder_permissions')
    can_view = models.BooleanField(default=True)
    can_edit = models.BooleanField(default=False)
    can_upload = models.BooleanField(default=False)

    class Meta:
        unique_together = ('folder', 'user')

    def __str__(self):
        return f"{self.user.username} on {self.folder.name}"

class ChunkedUpload(models.Model):
    upload_id = models.UUIDField(unique=True)
    file = models.FileField(upload_to='chunked_uploads/%Y/%m/%d/')
    offset = models.PositiveBigIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chunked_uploads')
    status = models.CharField(max_length=20, default='IN_PROGRESS') # IN_PROGRESS, COMPLETE
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chunk {self.offset} for {self.upload_id}"
