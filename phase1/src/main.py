import sys
import os

# Set base path and insert to sys.path before local imports
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_path)

import yaml
from context.context_engine import ContextEngine
from context.reasoning import ReasoningEngine
from context.interaction_logic import InteractionLogic
from memory.session_memory import SessionMemory
from memory.long_term_memory import LongTermMemory
from memory.conversation_tracker import ConversationTracker
from ethics.ethical_assessment import assess_ethics
from src.doctrine_loader import DoctrineLoader

# Load configuration
try:
    config_path = os.path.join(base_path, "config.yaml")
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    print("Configuration loaded successfully.")
except FileNotFoundError:
    print("Error: Configuration file not found.")
    exit(1)

# Initialize Echo's components
try:
    session_memory = SessionMemory(os.path.join(base_path, "memory/session_memory.json"))
    long_term_memory = LongTermMemory(os.path.join(base_path, "memory/long_term_memory.json"))
    conversation_tracker = ConversationTracker()

    doctrine_path = os.path.join(base_path, "doctrine")
    doctrine_loader = DoctrineLoader(doctrine_path)
    doctrine_loader.load_all()

    context_engine = ContextEngine(config)
    reasoning_engine = ReasoningEngine(context_engine.load_context())
    interaction_logic = InteractionLogic(session_memory, long_term_memory, doctrine_loader)

    print("Echo AGI Initialized: Ready for interaction.")
    print("\n🧠 Echo Doctrine Summary:")
    for title, excerpt in doctrine_loader.summarize().items():
        print(f"\n📜 {title}\n{excerpt}\n")

except Exception as e:
    print(f"Initialization failed: {e}")
    exit(1)

def interact(input_text):
    try:
        # Log user message
        conversation_tracker.log_turn("user", input_text)

        # Reasoning and response
        reasoning_steps = reasoning_engine.multi_step_reasoning(input_text)
        response = interaction_logic.generate_response(input_text)

        # Log Echo's response
        conversation_tracker.log_turn("echo", response)

        # Ethical check
        ethics_result = assess_ethics("truth", reasoning_steps[0])

        # Update short-term memory and log
        context_engine.update_short_term(input_text)
        reasoning_engine.log_reasoning(reasoning_steps)

        # Display response
        print(f"Echo: {response}")
        print(f"Ethics: {ethics_result}")

        # Show recent dialogue summary
        print("\n🧠 Recent Dialogue:")
        for line in conversation_tracker.summary():
            print(f"- {line}")

    except Exception as e:
        print(f"Error during interaction: {e}")

# Main interaction loop
if __name__ == "__main__":
    print("Echo: Ready for input.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Echo: Goodbye.")
                break
            interact(user_input)
        except KeyboardInterrupt:
            print("\nEcho: Exiting gracefully.")
            break
