import time
import logging
from typing import AsyncGenerator
from anthropic import AsyncAnthropic
from backend.app.llm.base import BaseLLMProvider
from backend.app.llm.models import LLMRequest, LLMResponse, LLMUsage
from backend.app.llm.exceptions import (
    AuthenticationError, RateLimitError, LLMTimeout, LLMGenerationError
)
from backend.app.config.settings import settings

logger = logging.getLogger("ai_lecture_assistant")

class AnthropicProvider(BaseLLMProvider):
    """
    Adapter for Anthropic Claude LLMs.
    """

    def __init__(self):
        api_key = settings.ai.anthropic_api_key
        if not api_key:
            self.client = None
        else:
            self.client = AsyncAnthropic(api_key=api_key)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        if not self.client:
            raise AuthenticationError("Anthropic API key not configured")

        start_time = time.perf_counter()
        try:
            response = await self.client.messages.create(
                model=request.model or "claude-3-5-sonnet-20240620",
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                system=request.system_prompt,
                messages=[{"role": "user", "content": request.prompt}]
            )

            latency = time.perf_counter() - start_time

            return LLMResponse(
                text=response.content[0].text,
                provider="anthropic",
                model=response.model,
                usage=LLMUsage(
                    prompt_tokens=response.usage.input_tokens,
                    completion_tokens=response.usage.output_tokens,
                    total_tokens=response.usage.input_tokens + response.usage.output_tokens
                ),
                latency=latency,
                finish_reason=response.stop_reason or "stop"
            )
        except Exception as e:
            self._handle_exception(e)

    async def stream_generate(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        if not self.client:
            raise AuthenticationError("Anthropic API key not configured")

        try:
            async with self.client.messages.stream(
                model=request.model or "claude-3-5-sonnet-20240620",
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                system=request.system_prompt,
                messages=[{"role": "user", "content": request.prompt}]
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception as e:
            self._handle_exception(e)

    async def health_check(self) -> bool:
        if not self.client:
            return False
        try:
            # Anthropic doesn't have a lightweight health check endpoint
            # We simulate one by sending a very short request
            await self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1,
                messages=[{"role": "user", "content": "ping"}]
            )
            return True
        except Exception:
            return False

    def count_tokens(self, text: str) -> int:
        # Simplified estimation: approx 4 chars per token
        return len(text) // 4

    def _handle_exception(self, e: Exception):
        import anthropic
        if isinstance(e, anthropic.RateLimitError):
            raise RateLimitError(str(e))
        if isinstance(e, anthropic.AuthenticationError):
            raise AuthenticationError(str(e))
        if isinstance(e, anthropic.APIConnectionError):
            raise LLMTimeout(str(e))
        raise LLMGenerationError(str(e))
