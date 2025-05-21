import os
from datetime import datetime

class ReasoningEngine:
    def __init__(self, context):
        self.context = context
        # Set the log path directly
        base_path = os.path.dirname(os.path.dirname(__file__))
        self.log_path = os.path.join(base_path, "logs/interaction.log")
        self.ensure_log_file(self.log_path)

    # Ensure the log file and directory exist
    def ensure_log_file(self, path):
        try:
            # Get the directory from the path
            directory = os.path.dirname(path)
            # Create the directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created log directory: {directory}")
            # Create the file if it doesn't exist
            if not os.path.isfile(path):
                with open(path, 'w') as f:
                    f.write("")  # Create an empty log file
                print(f"Created log file: {path}")
        except Exception as e:
            print(f"Error ensuring log file: {e}")

    # Multi-step reasoning simulation
    def multi_step_reasoning(self, input_text):
        # Simulate multi-step reasoning
        steps = []
        for i in range(3):
            step = f"Step {i+1}: Analyzing - {input_text}"
            steps.append(step)
        return steps

    # Log reasoning steps to the interaction log
    def log_reasoning(self, steps):
        try:
            with open(self.log_path, 'a') as log_file:
                log_file.write(f"Reasoning Process - {datetime.now().isoformat()}:\n")
                for step in steps:
                    log_file.write(f"{step}\n")
                log_file.write("\n")
            print(f"Logged reasoning steps to: {self.log_path}")
        except Exception as e:
            print(f"Error logging reasoning: {e}")
