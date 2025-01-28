import os
from dotenv import load_dotenv
from os_computer_use.llm_provider import OpenAIBaseProvider, AnthropicBaseProvider
from os_computer_use.osatlas_provider import OSAtlasProvider
from os_computer_use.showui_provider import ShowUIProvider

# Load environment variables from .env file
load_dotenv()

# LLM providers use the OpenAI specification and require a base URL:
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

load_dotenv()

# OpenAI Provider (replacing others like Anthropic, Llama, etc.)
class OpenAIProvider(OpenAIBaseProvider):
    """
    OpenAI Provider using OpenAIBaseProvider for all LLM-related tasks.
    """
    base_url = "https://api.openai.com/v1"
    api_key = os.getenv("OPENAI_API_KEY")
    aliases = {
        "gpt-4": "gpt-4",
        "gpt-3.5-turbo": "gpt-3.5-turbo"
    }

class LlamaProvider(OpenAIBaseProvider):
    base_url = "https://api.llama-api.com"
    api_key = os.getenv("LLAMA_API_KEY")
    aliases = {"llama3.2": "llama3.2-90b-vision", "llama3.3": "llama3.3-70b"}


class OpenRouterProvider(OpenAIBaseProvider):
    base_url = "https://openrouter.ai/api/v1"
    api_key = os.getenv("OPENROUTER_API_KEY")
    aliases = {"llama3.2": "meta-llama/llama-3.2-90b-vision-instruct"}


class FireworksProvider(OpenAIBaseProvider):
    base_url = "https://api.fireworks.ai/inference/v1"
    api_key = os.getenv("FIREWORKS_API_KEY")
    aliases = {
        "llama3.2": "accounts/fireworks/models/llama-v3p2-90b-vision-instruct",
        "llama3.3": "accounts/fireworks/models/llama-v3p3-70b-instruct",
    }


class DeepSeekProvider(OpenAIBaseProvider):
    base_url = "https://api.deepseek.com"
    api_key = os.getenv("DEEPSEEK_API_KEY")


class OpenAIProvider(OpenAIBaseProvider):
    base_url = "https://api.openai.com/v1"
    api_key = os.getenv("OPENAI_API_KEY")


class GeminiProvider(OpenAIBaseProvider):
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
    api_key = os.getenv("GEMINI_API_KEY")


class AnthropicProvider(AnthropicBaseProvider):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    aliases = {
        "claude-3.5-sonnet": "claude-3-5-sonnet-20241022",
        "claude-3.5-haiku": "claude-3-5-haiku-20241022",
        "claude-3-opus": "claude-3-opus-20240229",
    }


class GroqProvider(OpenAIBaseProvider):
    base_url = "https://api.groq.com/openai/v1"
    api_key = os.getenv("GROQ_API_KEY")
    aliases = {"llama3.2": "llama-3.2-90b-vision-preview"}
