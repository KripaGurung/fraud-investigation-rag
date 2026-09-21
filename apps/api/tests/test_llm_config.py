from api.core.config import settings


def test_openai_configuration_has_safe_defaults() -> None:
    assert settings.openai_model == "gpt-5.6"
    assert settings.openai_api_key is None