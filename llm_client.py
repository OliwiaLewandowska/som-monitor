"""
LLM API Client for querying different providers
"""
import time
from abc import ABC, abstractmethod
from typing import Optional
import openai
from config import OPENAI_API_KEY, RATE_LIMIT_DELAY


class LLMClient(ABC):
    """Base class for LLM clients"""
    
    @abstractmethod
    def query(self, prompt: str, model: str, temperature: float, max_tokens: int) -> Optional[str]:
        """Query the LLM and return response"""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return provider name"""
        pass


class OpenAIClient(LLMClient):
    """OpenAI API Client"""
    
    def __init__(self, api_key: str = OPENAI_API_KEY):
        self.client = openai.OpenAI(api_key=api_key)
        self._provider_name = "openai"
    
    @property
    def provider_name(self) -> str:
        return self._provider_name
    
    def query(self, prompt: str, model: str = "gpt-4o", 
              temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
        """Query OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            time.sleep(RATE_LIMIT_DELAY)
            return response.choices[0].message.content
        except openai.APIError as e:
            print(f"OpenAI API error: {e}")
            return None
        except openai.RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
            time.sleep(5)
            return None
        except Exception as e:
            print(f"Unexpected error querying OpenAI: {e}")
            return None


class LLMClientFactory:
    """Factory for creating LLM clients"""
    
    _clients = {
        "openai": OpenAIClient
    }
    
    @classmethod
    def create(cls, provider: str, **kwargs) -> LLMClient:
        """Create an LLM client for the specified provider"""
        if provider not in cls._clients:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(cls._clients.keys())}")
        
        return cls._clients[provider](**kwargs)
    
    @classmethod
    def register(cls, provider: str, client_class: type):
        """Register a new LLM client"""
        cls._clients[provider] = client_class
