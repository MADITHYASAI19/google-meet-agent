import time
import logging
from typing import AsyncGenerator
import google.generativeai as genai
from backend.app.llm.base import BaseLLMProvider
from backend.app.llm.models import LLMRequest, LLMResponse, LLMUsage
from backend.app.llm.exceptions import (
    AuthenticationError, RateLimitError, LLMTimeout, LLMGenerationError
)
from backend.app.config.settings import settings

logger = logging.getLogger("ai_lecture_assistant")

class GeminiProvider(BaseLLMProvider):
    """
    Adapter for Google Gemini LLMs.
    """

    def __init__(self):
        api_key = settings.ai.gemini_api_key
        if not api_key:
            self.client = None
        else:
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel

    async def generate(self, request: LLMRequest) -> LLMResponse:
        if not self.client:
            raise AuthenticationError("Gemini API key not configured")

        start_time = time.perf_counter()
        try:
            model = self.client(model_name=request.model or "gemini-1.5-flash")

            # Gemini handles system prompts differently
            # We use the system_instruction parameter in the constructor
            if request.system_prompt:
                model = self.client(
                    model_name=request.model or "gemini-1.5-flash",
                    system_instruction=request.system_prompt
                )

            response = await model.generate_content_async(
                request.prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=request.temperature,
                    top_p=request.top_p,
                    max_output_tokens=request.max_tokens,
                    stop_sequences=request.stop_sequences
                )
            )

            latency = time.perf_counter() - start_time

            # Gemini usage is in response.usage_metadata
            usage = response.usage_metadata

            return LLMResponse(
                text=response.text,
                provider="gemini",
                model=request.model or "gemini-1.5-flash",
                usage=LLMUsage(
                    prompt_tokens=usage.prompt_token_count,
                    completion_tokens=usage.candidates_token_count,
                    total_tokens=usage.total_token_count
                ),
                latency=latency,
                finish_reason="stop" # Gemini doesn't provide a standard finish_reason string
            )
        except Exception as e:
            self._handle_exception(e)

    async def stream_generate(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        if not self.client:
            raise AuthenticationError("Gemini API key not configured")

        model = self.client(
            model_name=request.model or "gemini-1.5-flash",
            system_instruction=request.system_prompt
        )

        try:
            response = await model.generate_content_async(
                request.prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=request.temperature,
                    top_p=request.top_p,
                    max_output_tokens=request.max_tokens,
                    stop_sequences=request.stop_sequences
                ),
                stream=True
            )

            async for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            self._handle_exception(e)

    async def health_check(self) -> bool:
        if not self.client:
            return False
        try:
            # Minimal check: list models
            genai.list_models()
            return True
        except Exception:
            return False

    def count_tokens(self, text: str) -> int:
        # Gemini has a specific count_tokens method
        if not self.client:
            return len(text) // 4
        try:
            model = self.client(model_name="gemini-1.5-flash")
            return model.count_tokens(text).total_tokens
        except Exception:
            return len(text) // 4

    def _handle_exception(self, e: Exception):
        # Google AI SDK exceptions are less standardized than OpenAI/Anthropic
        err_msg = str(e).lower()
        if "429" in err_msg or "quota" in err_msg:
            raise RateLimitError(str(e))
        if "401" in err_msg or "api key" in err_msg:
            raise AuthenticationError(str(e))
        raise LLMGenerationError(str(e))
