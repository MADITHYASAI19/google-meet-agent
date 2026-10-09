import time
import logging
import asyncio
from typing import AsyncGenerator, List, Optional
from backend.app.llm.base import BaseLLMProvider
from backend.app.llm.models import LLMRequest, LLMResponse
from backend.app.llm.provider_factory import ProviderFactory
from backend.app.llm.exceptions import (
    ProviderUnavailable, LLMTimeout, LLMGenerationError, InvalidProvider
)
from backend.app.config.settings import settings

logger = logging.getLogger("ai_lecture_assistant")

class LLMRouter:
    """
    The central entry point for all AI requests in the system.
    Handles provider selection, fallbacks, retries, and observability.
    """

    def __init__(self):
        self.factory = ProviderFactory()

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generates a response using the default provider, with fallback support.
        """
        # Determine the sequence of providers to try
        providers_to_try = [settings.ai.default_provider] + settings.ai.fallback_providers

        last_exception = None

        for provider_name in providers_to_try:
            try:
                return await self._execute_with_retry(provider_name, request)
            except (ProviderUnavailable, LLMTimeout, LLMGenerationError, RateLimitError) as e:
                logger.warning(f"[LLM_ROUTER] Provider {provider_name} failed: {str(e)}. Trying next fallback...")
                last_exception = e
                continue
            except Exception as e:
                logger.error(f"[LLM_ROUTER] Unexpected error with provider {provider_name}: {str(e)}")
                last_exception = e
                continue

        # All providers failed
        if last_exception:
            raise last_exception
        raise ProviderUnavailable("All configured LLM providers failed to respond.")

    async def _execute_with_retry(self, provider_name: str, request: LLMRequest) -> LLMResponse:
        """
        Handles the retry logic for a single provider.
        """
        provider = self.factory.get_provider(provider_name)

        for attempt in range(settings.ai.max_retries):
            try:
                start_time = time.perf_counter()
                response = await provider.generate(request)
                latency = time.perf_counter() - start_time

                # Log success
                logger.info(
                    f"[LLM_ROUTER] Success | Provider: {provider_name} | "
                    f"Model: {response.model} | Latency: {latency:.2f}s | "
                    f"Tokens: {response.usage.total_tokens}"
                )
                return response
            except Exception as e:
                if attempt == settings.ai.max_retries - 1:
                    raise e

                logger.warning(f"[LLM_ROUTER] Attempt {attempt+1} failed for {provider_name}: {str(e)}. Retrying...")
                await asyncio.sleep(settings.ai.retry_delay)

    async def stream_generate(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """
        Streams a response from the default provider.
        Note: Fallback is more complex for streaming; we use the primary provider.
        """
        provider = self.factory.get_provider(settings.ai.default_provider)
        async for chunk in provider.stream_generate(request):
            yield chunk

    async def health(self) -> Dict[str, bool]:
        """
        Returns the health status of all registered providers.
        """
        results = {}
        # We only check providers configured in settings
        providers_to_check = [settings.ai.default_provider] + settings.ai.fallback_providers

        for name in providers_to_check:
            try:
                provider = self.factory.get_provider(name)
                results[name] = await provider.health_check()
            except Exception:
                results[name] = False

        return results

llm_router = LLMRouter()
