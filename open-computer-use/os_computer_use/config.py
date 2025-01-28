from os_computer_use import providers

# Replace Anthropic with OpenAIProvider
grounding_model = providers.OSAtlasProvider()
vision_model = providers.OpenAIProvider("gpt-4")  # Use GPT-4 from OpenAI
action_model = providers.OpenAIProvider("gpt-4")  # Use GPT-4 from OpenAI
