from faster_whisper import WhisperModel
import os

class WhisperService:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        # In production, device should be "cuda" if GPU is available.
        # compute_type="int8" is good for CPU/low-resource.
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, file_path):
        """
        Transcribes the given audio/video file.
        Returns a dictionary with text and segments.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        segments, info = self.model.transcribe(file_path, beam_size=5)
        
        # Collect segments generator into a list
        segment_list = []
        full_text = ""
        
        for segment in segments:
            segment_data = {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            }
            segment_list.append(segment_data)
            full_text += segment.text + " "

        return {
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "text": full_text.strip(),
            "segments": segment_list
        }
