import time

from groq import RateLimitError
from langchain_groq import ChatGroq

from app.core.config import settings


class LLMClient:
    """Wraps ChatGroq (via LangChain) for generating answers from prompts."""

    def __init__(self):
        self.llm = ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key,
        )

    def generate(self, prompt: str, max_retries: int = 5) -> str:
        """Sends a prompt to Groq and returns the generated answer text.
        Retries with exponential backoff if rate-limited."""

        delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                response = self.llm.invoke(prompt)
                content = response.content

                if isinstance(content, list):
                    # Some providers can return content as a list of parts instead of a plain string
                    content = "".join(
                        part.get("text", "") if isinstance(part, dict) else str(part)
                        for part in content
                    )

                return content
            except RateLimitError:
                is_last_attempt = attempt == max_retries - 1

                if is_last_attempt:
                    raise

                print(f"Rate limited. Waiting {delay}s before retry ({attempt + 1}/{max_retries})...")
                time.sleep(delay)
                delay *= 2

        raise RuntimeError("Exceeded max retries due to rate limiting.")
