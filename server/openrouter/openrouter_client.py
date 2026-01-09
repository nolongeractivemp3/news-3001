from typing import Optional

from openai import OpenAI


def query_openrouter(
    query: str,
    api_key: str,
    model: str = "mistralai/devstral-2512:free",
    system_prompt: Optional[str] = None,
    site_name: Optional[str] = None,
) -> str:
    """
    Queries the OpenRouter API with a given query and API key.

    Args:
        query: The query or prompt to send to the OpenRouter API.
        api_key: The API key for authenticating with OpenRouter.
        model: The model to use for the query. Defaults to "mistralai/devstral-2512:free".
        system_prompt: Optional. System prompt to guide the behavior of the model.
        site_name: Optional. Site title for rankings on openrouter.ai.

    Returns:
        The response content from the OpenRouter API.
    """
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    if not system_prompt:
        system_prompt = "You are a helpful assistant."
    extra_headers = {}
    if site_name:
        extra_headers["X-Title"] = site_name

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]
    completion = client.chat.completions.create(
        extra_headers=extra_headers,
        extra_body={},
        model=model,
        messages=messages,
    )

    return completion.choices[0].message.content
