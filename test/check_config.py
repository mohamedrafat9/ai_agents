from config import get_settings


settings = get_settings()

print("Provider:", settings.default_provider)
print("OpenRouter model:", settings.openrouter_model)
print("OpenAI model:", settings.openai_model)
print("xAI model:", settings.xai_model)
print("Google model:", settings.google_model)