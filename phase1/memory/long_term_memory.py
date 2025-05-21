import json
import os

class LongTermMemory:
    def __init__(self, path):
        self.path = path
        self.memory = self.load_memory()

    def load_memory(self):
        if not os.path.exists(self.path):
            return {}
        try:
            with open(self.path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading long-term memory: {e}")
            return {}

    def save_memory(self):
        try:
            with open(self.path, 'w') as file:
                json.dump(self.memory, file, indent=4)
        except Exception as e:
            print(f"Error saving long-term memory: {e}")

    def update(self, key, value):
        self.memory[key] = value
        self.save_memory()

    def recall(self, key):
        return self.memory.get(key, None)

    def clear(self):
        self.memory = {}
        self.save_memory()
