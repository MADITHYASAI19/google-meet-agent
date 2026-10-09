from typing import Dict, Type
from backend.app.llm.base import BaseLLMProvider
from backend.app.llm.providers.openai_provider import OpenAIProvider
from backend.app.llm.providers.anthropic_provider import AnthropicProvider
from backend.app.llm.providers.gemini_provider import GeminiProvider
from backend.app.llm.providers.grok_provider import GrokProvider
from backend.app.config.settings import settings

class ProviderFactory:
    """
    Factory for creating LLM providers based on configuration.
    """

    _PROVIDERS: Dict[str, Type[BaseLLMProvider]] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
        "grok": GrokProvider,
        "claude": AnthropicProvider # Alias
    }

    @classmethod
    def get_provider(cls, provider_name: str) -> BaseLLMProvider:
        """
        Instantiates and returns the requested LLM provider.
        """
        provider_class = cls._PROVIDERS.get(provider_name.lower())
        if not provider_class:
            from backend.app.llm.exceptions import InvalidProvider
            raise InvalidProvider(f"Provider '{provider_name}' is not supported.")

        return provider_class()
