from abc import ABC, abstractmethod
from typing import AsyncGenerator
from backend.app.llm.models import LLMRequest, LLMResponse

class BaseLLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    Every provider must implement this interface to ensure the Router remains provider-agnostic.
    """

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate a non-streaming response from the LLM.
        """
        pass

    @abstractmethod
    async def stream_generate(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response from the LLM.
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check the health and connectivity of the provider's API.
        """
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in the given text using provider-specific logic.
        """
        pass
