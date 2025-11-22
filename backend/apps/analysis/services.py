import google.generativeai as genai
from django.conf import settings
import requests
import json

class LLMService:
    def __init__(self):
        self.provider = getattr(settings, 'LLM_PROVIDER', 'gemini')
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        self.api_url = getattr(settings, 'LLM_API_URL', 'http://localhost:11434/v1')
        self.model_name = getattr(settings, 'LLM_MODEL_NAME', 'gemini-1.5-flash')

        if self.provider == 'gemini' and self.api_key:
            genai.configure(api_key=self.api_key)

    def generate(self, prompt, system_prompt=None):
        """
        Generates text based on the prompt using the configured provider.
        """
        full_prompt = prompt
        if system_prompt:
            # For some models, system prompt is separate. For simplicity, we prepend it.
            # Gemini supports system instructions, but for generic compatibility let's prepend.
            # Actually, let's try to use provider-specific best practices.
            pass

        if self.provider == 'gemini':
            return self._generate_gemini(prompt, system_prompt)
        elif self.provider == 'local':
            return self._generate_local(prompt, system_prompt)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _generate_gemini(self, prompt, system_prompt=None):
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        
        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    def _generate_local(self, prompt, system_prompt=None):
        """
        Connects to an OpenAI-compatible API (like Ollama).
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False
        }

        try:
            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
             raise Exception(f"Local LLM API error: {str(e)}")
