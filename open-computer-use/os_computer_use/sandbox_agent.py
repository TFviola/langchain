import pyautogui
import os
import tempfile
import json
from os_computer_use.logging import logger

TYPING_DELAY_MS = 12
TYPING_GROUP_SIZE = 50

tools = {
    "stop": {
        "description": "Indicate that the task has been completed.",
        "params": {},
    },
    "run_command": {
        "description": "Run a shell command.",
        "params": {"command": "The command to run"},
    },
    "run_background_command": {
        "description": "Run a shell command in the background.",
        "params": {"command": "The command to run"},
    },
    "send_key": {
        "description": "Send a key or combination of keys to the system.",
        "params": {"name": "The key or key combination (e.g., 'Ctrl-C')"},
    },
    "type_text": {
        "description": "Type a specified text into the system.",
        "params": {"text": "The text to type"},
    },
    "click": {
        "description": "Click on a specified UI element.",
        "params": {"query": "The element or location to click"},
    },
    "double_click": {
        "description": "Double-click on a specified UI element.",
        "params": {"query": "The element or location to double-click"},
    },
    "right_click": {
        "description": "Right-click on a specified UI element.",
        "params": {"query": "The element or location to right-click"},
    },
}


class SandboxAgent:
    def __init__(self, output_dir="."):
        """
        Initialize the SandboxAgent.
        """
        self.output_dir = output_dir
        self.tmp_dir = tempfile.mkdtemp()
        self.messages = []
        logger.log("SandboxAgent initialized successfully.", "green")

        # Display available actions
        print("The agent will use the following actions:")
        for action, details in tools.items():
            print(f"- {action}({', '.join(details['params'].keys())})")

    def take_screenshot(self):
        """
        Take a screenshot of the desktop.
        """
        screenshot = pyautogui.screenshot()
        screenshot_path = os.path.join(self.tmp_dir, "screenshot.png")
        screenshot.save(screenshot_path)
        logger.log(f"Screenshot saved: {screenshot_path}", "gray")
        return screenshot_path

    def run_command(self, command):
        """
        Run a shell command and return the result.
        """
        os.system(command)
        logger.log(f"Command executed: {command}", "green")

    def type_text(self, text):
        """
        Type text character by character.
        """
        pyautogui.typewrite(text, interval=0.05)
        logger.log(f"Typed text: {text}", "green")

    def send_key(self, name):
        """
        Send a key or key combination.
        """
        keys = name.split("-")
        pyautogui.hotkey(*keys)
        logger.log(f"Sent key combination: {name}", "green")

    def click(self, query):
        """
        Click on a specified UI element or location.
        """
        # This is a simplified example; you can expand it to locate UI elements visually
        logger.log(f"Clicking at location: {query} (not implemented fully)", "yellow")
        pyautogui.click()

    def double_click(self, query):
        """
        Double-click on a specified UI element or location.
        """
        logger.log(f"Double-clicking at location: {query} (not implemented fully)", "yellow")
        pyautogui.doubleClick()

    def right_click(self, query):
        """
        Right-click on a specified UI element or location.
        """
        logger.log(f"Right-clicking at location: {query} (not implemented fully)", "yellow")
        pyautogui.rightClick()

    def process_user_input(self, user_input):
        """
        Parse and execute the user input.
        """
        try:
            # Strip input and split it into an action and parameters
            parts = user_input.strip().split(" ", 1)
            action = parts[0].strip().lower()

            # Handle actions with no parameters (e.g., stop)
            params = json.loads(parts[1].strip()) if len(parts) > 1 else {}

            if action in tools:
                logger.log(f"Executing action: {action} with params: {params}", "blue")
                if action == "run_command":
                    self.run_command(params.get("command", ""))
                elif action == "type_text":
                    self.type_text(params.get("text", ""))
                elif action == "send_key":
                    self.send_key(params.get("name", ""))
                elif action == "click":
                    self.click(params.get("query", ""))
                elif action == "double_click":
                    self.double_click(params.get("query", ""))
                elif action == "right_click":
                    self.right_click(params.get("query", ""))
                elif action == "stop":
                    logger.log("Task completed. Stopping agent.", "yellow")
                    return False  # Stop the loop
            else:
                logger.log(f"Unknown action: {action}", "red")
        except json.JSONDecodeError:
            logger.log("Error: Invalid JSON format. Please provide parameters in JSON format.", "red")
        except Exception as e:
            logger.log(f"Error processing input: {str(e)}", "red")

        return True  # Continue the loop
