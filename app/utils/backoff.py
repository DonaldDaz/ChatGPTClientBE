from tenacity import retry, wait_exponential_jitter, stop_after_attempt, retry_if_exception_type
from openai import RateLimitError, APIError

def openai_retry():
    return retry(
        wait=wait_exponential_jitter(initial=1, max=8),
        stop=stop_after_attempt(6),
        retry=retry_if_exception_type((RateLimitError, APIError)),
        reraise=True
    )
