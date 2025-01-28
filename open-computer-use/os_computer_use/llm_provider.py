from openai import OpenAI
import json
import re
import base64


def Message(content, role="assistant"):
    """
    Create a message object for use in LLM requests.
    """
    return {"role": role, "content": content}


def Text(text):
    """
    Create a text block for a message.
    """
    return {"type": "text", "text": text}


def parse_json(s):
    """
    Safely parse a JSON string into a Python dictionary.
    """
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {s}")
        return {}


class LLMProvider:
    """
    A base class for interacting with language models (LLMs).
    """

    # Class attributes for base URL and API key
    base_url = None
    api_key = None

    # Mapping of model aliases
    aliases = {}

    def __init__(self, model):
        """
        Initialize the LLM provider with the specified model.
        """
        self.model = self.aliases.get(model, model)
        print(f"Using {self.__class__.__name__} with {self.model}")
        self.client = self.create_client()

    def create_function_schema(self, definitions):
        """
        Convert function definitions into a provider-specific schema.
        """
        functions = []
        for name, details in definitions.items():
            properties = {
                param_name: {"type": "string", "description": param_desc}
                for param_name, param_desc in details["params"].items()
            }
            required = list(details["params"].keys())
            functions.append(self.create_function_def(name, details, properties, required))
        return functions

    def wrap_block(self, block):
        """
        Wrap a content block (text or image) for use in LLM messages.
        """
        if isinstance(block, bytes):
            encoded_image = base64.b64encode(block).decode("utf-8")
            return self.create_image_block(encoded_image)
        else:
            return Text(block)

    def transform_message(self, message):
        """
        Wrap content blocks in image or text objects.
        """
        content = message["content"]
        if isinstance(content, list):
            wrapped_content = [self.wrap_block(block) for block in content]
            return {**message, "content": wrapped_content}
        else:
            return message

    def completion(self, messages, **kwargs):
        """
        Call the LLM to generate a response.
        """
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        new_messages = [self.transform_message(message) for message in messages]
        completion = self.client.create(messages=new_messages, model=self.model, **filtered_kwargs)

        if hasattr(completion, "error"):
            raise Exception(f"Error calling model: {completion.error}")
        return completion


class OpenAIBaseProvider(LLMProvider):
    """
    A provider for OpenAI's language models.
    """

    def create_client(self):
        """
        Initialize the OpenAI client.
        """
        try:
            return OpenAI(base_url=self.base_url, api_key=self.api_key).chat.completions
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            raise

    def create_function_def(self, name, details, properties, required):
        """
        Create a function definition for the OpenAI API.
        """
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": details["description"],
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }

    def create_image_block(self, base64_image):
        """
        Wrap an image in a base64-encoded block.
        """
        return {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}

    def call(self, messages, functions=None):
        """
        Make a call to the OpenAI API and handle responses.
        """
        tools = self.create_function_schema(functions) if functions else None
        completion = self.completion(messages, tools=tools)
        message = completion.choices[0].message

        if functions:
            tool_calls = message.tool_calls or []
            combined_tool_calls = [
                {
                    "type": "function",
                    "name": tool_call.function.name,
                    "parameters": parse_json(tool_call.function.arguments),
                }
                for tool_call in tool_calls
                if parse_json(tool_call.function.arguments) is not None
            ]

            # Parse additional tool calls manually if necessary
            if message.content and not tool_calls:
                tool_call_match = re.search(r"\{.*\}", message.content)
                if tool_call_match:
                    tool_call = parse_json(tool_call_match.group(0))
                    if tool_call.get("name") and tool_call.get("parameters"):
                        combined_tool_calls.append(tool_call)

            return message.content, combined_tool_calls

        # Return only text if no functions are provided
        return message.content


# Add additional providers as needed, or remove unused ones
