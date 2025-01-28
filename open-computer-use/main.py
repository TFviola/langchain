import argparse
from os_computer_use.sandbox_agent import SandboxAgent
from os_computer_use.logging import Logger

logger = Logger()

def main():
    """
    Main entry point for the application.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, help="User prompt for the agent")
    args = parser.parse_args()

    agent = SandboxAgent(output_dir="./output")

    print("Waiting for user input. Type 'stop' to exit.")
    running = True

    while running:
        try:
            user_input = input("USER: ")
            if user_input.strip().lower() == "stop":
                running = False
                logger.log("Exiting on user request.", "yellow")
            else:
                running = agent.process_user_input(user_input)
        except KeyboardInterrupt:
            logger.log("Exiting on user interrupt.", "yellow")
            break

if __name__ == "__main__":
    main()
