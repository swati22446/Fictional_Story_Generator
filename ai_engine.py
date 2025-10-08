# ===================================================================
# FILE: ai_engine.py (FIXED VERSION with Updated Google API)
# ===================================================================
# AI integration for story generation using various APIs

import requests
import json
from typing import Optional
import FictionalStory_AI.config as config

class AIStoryEngine:
    def __init__(self, provider: str = None):
        """Initialize AI engine with specified provider"""
        self.provider = provider or config.DEFAULT_PROVIDER
        self.api_key = self._get_api_key()
        
    def _get_api_key(self):
        """Get API key based on provider"""
        if self.provider == "openai":
            return config.OPENAI_API_KEY
        elif self.provider == "anthropic":
            return config.ANTHROPIC_API_KEY
        elif self.provider == "google":
            return config.GOOGLE_API_KEY
        return None
    
    def generate_story(self, prompt: str, max_tokens: int = None) -> str:
        """Generate story using selected AI provider"""
        max_tokens = max_tokens or config.MAX_TOKENS
        
        try:
            if self.provider == "openai":
                return self._generate_openai(prompt, max_tokens)
            elif self.provider == "anthropic":
                return self._generate_anthropic(prompt, max_tokens)
            elif self.provider == "google":
                return self._generate_google(prompt, max_tokens)
            elif self.provider == "local":
                return self._generate_local(prompt)
            else:
                return "Error: Invalid AI provider selected."
        except Exception as e:
            return f"Error generating story: {str(e)}\n\nPlease check your API key in config.py"
    
    def _generate_openai(self, prompt: str, max_tokens: int) -> str:
        """Generate using OpenAI GPT"""
        if not self.api_key or self.api_key == "your-openai-api-key-here":
            return self._generate_local(prompt)
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": config.OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a creative fiction writer who crafts engaging, well-structured stories."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": config.TEMPERATURE
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    
    def _generate_anthropic(self, prompt: str, max_tokens: int) -> str:
        """Generate using Anthropic Claude"""
        if not self.api_key or self.api_key == "your-anthropic-api-key-here":
            return self._generate_local(prompt)
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": config.ANTHROPIC_MODEL,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": config.TEMPERATURE
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return result['content'][0]['text'].strip()
    
    def _generate_google(self, prompt: str, max_tokens: int) -> str:
        """Generate using Google Gemini (FIXED VERSION)"""
        if not self.api_key or self.api_key == "your-google-api-key-here":
            return self._generate_local(prompt)
        
        # Updated endpoint for Gemini Pro
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": config.TEMPERATURE,
                "maxOutputTokens": max_tokens,
                "topP": 0.95,
                "topK": 40
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            # Handle the response structure
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    return candidate['content']['parts'][0]['text'].strip()
            
            return "Error: Unexpected response format from Google API"
            
        except requests.exceptions.HTTPError as e:
            # Better error handling
            error_message = f"Google API Error: {e}"
            if response.text:
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        error_message = f"Google API Error: {error_data['error'].get('message', str(e))}"
                except:
                    pass
            return error_message
    
    def _generate_local(self, prompt: str) -> str:
        """Fallback local generation (demo mode without API)"""
        return """[DEMO MODE - No API Key Configured]

This is a demonstration of how the story would appear. To generate real AI-powered stories, please:

1. Open config.py
2. Add your API key from OpenAI, Anthropic, or Google
3. The application will then generate creative stories using AI

Your prompt was:
""" + prompt + """

To get started:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Google AI: https://aistudio.google.com/app/apikey

Once configured, the AI will generate unique, creative stories based on your inputs!"""