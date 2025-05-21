import os
import json
from datetime import datetime

class ContextEngine:
    def __init__(self, config):
        base_path = os.path.dirname(os.path.dirname(__file__))
        self.long_term_path = os.path.join(base_path, config["memory"]["long_term_path"])
        self.short_term_path = os.path.join(base_path, config["memory"]["short_term_path"])
        self.context_cache_path = os.path.join(base_path, config["memory"]["context_cache_path"])
        self.log_path = os.path.join(base_path, config["logging"]["interaction_log"])

        # Ensure necessary directories and files exist
        print("Calling ensure_file_exists for path:", self.long_term_path)
        self.ensure_file_exists(self.long_term_path)
        print("Calling ensure_file_exists for path:", self.short_term_path)
        self.ensure_file_exists(self.short_term_path)
        print("Calling ensure_file_exists for path:", self.context_cache_path)
        self.ensure_file_exists(self.context_cache_path)
        print("Calling ensure_file_exists for path:", self.log_path)
        self.ensure_file_exists(self.log_path)

    # Method to ensure directory and file exist
    def ensure_file_exists(self, path):
        directory = os.path.dirname(path)
    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

        # Create the file if it doesn't exist
        if not os.path.isfile(path):
            with open(path, 'w') as f:
                # Create an empty JSON object for memory files
                if path.endswith(".json"):
                    json.dump({"conversations": []}, f)  # Initialize with an empty list for conversations
                else:
                    f.write("")  # Create an empty file for logs
            print(f"Created file: {path}")
    except Exception as e:
        print(f"Error creating file or directory: {e}")

    def load_context(self):
        try:
            with open(self.context_cache_path, 'r') as file:
                return json.load(file).get("recent_contexts", [])
        except FileNotFoundError:
            return []

    def save_context(self, context):
        data = {"recent_contexts": context, "cache_size": len(context)}
        with open(self.context_cache_path, 'w') as file:
            json.dump(data, file, indent=4)

    def update_short_term(self, message):
        try:
            with open(self.short_term_path, 'r') as file:
                data = json.load(file)
            data.setdefault("conversations", []).append({"message": message, "timestamp": datetime.now().isoformat()})
            with open(self.short_term_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error updating short-term memory: {e}")

    def log_reasoning(self, steps):
        try:
            with open(self.log_path, 'a') as log_file:
                log_file.write(f"Reasoning Process - {datetime.now().isoformat()}:\n")
                for step in steps:
                    log_file.write(f"{step}\n")
                log_file.write("\n")
        except Exception as e:
            print(f"Error logging reasoning: {e}")
