from typing import Optional
class ProviderUnavailable(Exception):
    """Raised when the selected provider is not available or configured."""
    pass

class InvalidProvider(Exception):
    """Raised when an requested provider is not registered in the factory."""
    pass

class AuthenticationError(Exception):
    """Raised when API keys are missing or invalid."""
    pass

class RateLimitError(Exception):
    """Raised when the provider returns a rate limit error."""
    pass

class LLMTimeout(Exception):
    """Raised when a provider request times out."""
    pass

class LLMGenerationError(Exception):
    """Raised when the LLM fails to generate a response."""
    pass
