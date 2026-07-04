import os
import yaml
import requests
from typing import List, Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class LLMProvider:
    def __init__(self, config: Dict[str, Any]):
        self.name = config['name']
        # Allow endpoint override via environment variable (e.g. 9ROUTER_ENDPOINT=http://localhost:8000)
        env_endpoint = os.getenv(f"{self.name.upper()}_ENDPOINT")
        self.endpoint = env_endpoint if env_endpoint else config['endpoint']
        
        self.api_key = os.getenv(config['api_key_env'])
        self.models = {m['id']: m['role'] for m in config['models']}

    def call(self, model_id: str, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 4000) -> str:
        if not self.api_key:
            # Return a mock response for development if no key is found
            return f"[MOCK-9ROUTER] Response from {model_id}: This is a simulated response because {os.getenv('NINEROUTER_API_KEY', 'API KEY')} is not set. Prompt: {messages[-1]['content'][:50]}..."
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        url = self.endpoint.rstrip('/')
        if not url.endswith('/chat/completions'):
            url += '/chat/completions'

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"[ERROR] Call to {model_id} failed: {str(e)}"

class LLMRouter:
    def __init__(self, config_path: Path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.providers = [LLMProvider(p) for p in config['providers']]
        self.model_map = {}
        for p in self.providers:
            for mid, role in p.models.items():
                self.model_map[role] = (p, mid)

    def get_model_for_role(self, role: str) -> tuple[LLMProvider, str]:
        if role not in self.model_map:
            p = self.providers[0]
            mid = list(p.models.keys())[0]
            return p, mid
        return self.model_map[role]

    def generate(self, role: str, prompt: str, system_prompt: str = "You are a helpful assistant.", **kwargs) -> str:
        provider, model_id = self.get_model_for_role(role)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        return provider.call(model_id, messages, **kwargs)
