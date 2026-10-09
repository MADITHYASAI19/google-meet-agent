import time
import logging
from typing import AsyncGenerator
from openai import AsyncOpenAI
from backend.app.llm.base import BaseLLMProvider
from backend.app.llm.models import LLMRequest, LLMResponse, LLMUsage
from backend.app.llm.exceptions import (
    AuthenticationError, RateLimitError, LLMTimeout, LLMGenerationError
)
from backend.app.config.settings import settings

logger = logging.getLogger("ai_lecture_assistant")

class GrokProvider(BaseLLMProvider):
    """
    Adapter for Grok (xAI) LLMs.
    Grok uses an OpenAI-compatible API.
    """

    def __init__(self):
        api_key = settings.ai.grok_api_key
        base_url = settings.ai.grok_base_url

        if not api_key:
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        if not self.client:
            raise AuthenticationError("Grok API key not configured")

        start_time = time.perf_counter()
        try:
            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})

            response = await self.client.chat.completions.create(
                model=request.model or settings.ai.default_model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=request.top_p,
                stop=request.stop_sequences
            )

            latency = time.perf_counter() - start_time
            completion = response.choices[0].message.content

            return LLMResponse(
                text=completion or "",
                provider="grok",
                model=response.model,
                usage=LLMUsage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens
                ),
                latency=latency,
                finish_reason=response.choices[0].finish_reason or "stop"
            )
        except Exception as e:
            self._handle_exception(e)

    async def stream_generate(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        if not self.client:
            raise AuthenticationError("Grok API key not configured")

        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})

        try:
            response = await self.client.chat.completions.create(
                model=request.model or settings.ai.default_model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=request.top_p,
                stop=request.stop_sequences,
                stream=True
            )

            async for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            self._handle_exception(e)

    async def health_check(self) -> bool:
        if not self.client:
            return False
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False

    def count_tokens(self, text: str) -> int:
        return len(text) // 4

    def _handle_exception(self, e: Exception):
        import openai
        if isinstance(e, openai.RateLimitError):
            raise RateLimitError(str(e))
        if isinstance(e, openai.AuthenticationError):
            raise AuthenticationError(str(e))
        if isinstance(e, openai.APIConnectionError):
            raise LLMTimeout(str(e))
        raise LLMGenerationError(str(e))
