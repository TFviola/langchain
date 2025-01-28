import os

class Logger:
    color_map = {
        "black": "30", "red": "31", "green": "32", "yellow": "33",
        "blue": "34", "magenta": "35", "cyan": "36", "white": "37", "gray": "37;2",
    }

    css_color_map = {
        "black": ("#000000", "#e3f2fd"), "red": ("#8B0000", "#ffebee"),
        "green": ("#006400", "#e8f5e9"), "yellow": ("#8B8B00", "#fff3e0"),
        "blue": ("#00008B", "#e8eaf6"), "magenta": ("#8B008B", "#f5f5f5"),
        "cyan": ("#008B8B", "#f5f5f5"), "white": ("#CCCCCC", "#f5f5f5"),
        "gray": ("#666666", "#f5f5f5"),
    }

    def __init__(self):
        self.logs = []
        self.log_file = None
        self.log_file_template = None

        try:
            template_path = os.path.join(
                os.path.dirname(__file__), "templates", "log.html"
            )
            with open(template_path, "r") as f:
                self.log_file_template = f.read()
        except Exception as e:
            print(f"Warning: Could not load log template: {e}")

    def print_colored(self, message, color=None):
        color_code = self.color_map.get(color)
        if color_code:
            print(f"\033[{color_code}m{message}\033[0m")
        else:
            print(message)

    def write_log_file(self, logs, filepath):
        content = ""
        for entry in logs:
            color_info = self.css_color_map.get(
                entry["color"], (entry["color"], "#f5f5f5")
            )
            content += f"<p style='color:{color_info[0]};background:{color_info[1]}'>{entry['text']}</p>\n"

        with open(filepath, "w") as f:
            f.write(self.log_file_template.replace("{{content}}", content))

    def log(self, text, color="black", print=True):
        if print:
            self.print_colored(text, color)
        self.logs.append({"text": text, "color": color})
        if self.log_file:
            self.write_log_file(self.logs, self.log_file)
        return text

logger = Logger()
