from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_openrouter import ChatOpenRouter
from langchain_xai import ChatXAI

from config import get_settings


def get_llm(
    provider: str | None = None,
    model: str | None = None,
) -> BaseChatModel:
    settings = get_settings()

    selected_provider = (
        provider or settings.default_provider
    ).lower()

    if selected_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is missing")

        return ChatOpenAI(
            model=model or settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )

    if selected_provider == "xai":
        if not settings.xai_api_key:
            raise ValueError("XAI_API_KEY is missing")

        return ChatXAI(
            model=model or settings.xai_model,
            api_key=settings.xai_api_key,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )

    if selected_provider == "google":
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY is missing")

        return ChatGoogleGenerativeAI(
            model=model or settings.google_model,
            google_api_key=settings.google_api_key,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )

    if selected_provider == "openrouter":
        if not settings.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is missing")

        return ChatOpenRouter(
            model=model or settings.openrouter_model,
            api_key=settings.openrouter_api_key,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )
    if selected_provider == "groq":
        return ChatOpenAI(
            model=model or settings.groq_model,
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1",
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )

    raise ValueError(
        f"Unsupported provider: {selected_provider}"
    )