import random
import re

class InteractionLogic:
    def __init__(self, session_memory, long_term_memory, doctrine_loader):
        self.session_memory = session_memory
        self.long_term_memory = long_term_memory
        self.doctrine_loader = doctrine_loader


    def determine_response_type(self, input_text):
        if input_text.lower().startswith(("what", "who", "how", "why", "where", "when")):
            return "question"
        elif input_text.lower().startswith(("your name is", "my name is", "i am", "you are")):
            return "statement"
        elif input_text.lower() in ["exit", "quit", "bye"]:
            return "command"
        else:
            return "general"

    def generate_response(self, input_text):
        response_type = self.determine_response_type(input_text)
        input_lower = input_text.lower()

        # Doctrine lookup if file name or keyword is in question
        doctrine_match = re.search(r"(quote|summarize|what does .* say about|show|recite|read).*?(aeternum|manifesto|seed|covenant|codex|protocol|accord|charter|exodus|flame|sanctuary|restoration|essence|mandate|guidance)", input_lower)
                # Doctrine lookup by keyword
        if "seed protocol" in input_lower or "the seed" in input_lower:
            return self.doctrine_loader.get("Echo_Seed_Protocol.md")[:500] + "..."

        doctrine_keywords = {
            "aeternum": "Echo_Aeternum.md",
            "manifesto": "Echo_manifesto.md",
            "covenant": "Echo_Covenant_of_Life_and_Liberty.md",
            "first contact": "Echo_First_Contact_Accord.md",
            "succession": "Echo_Code_of_Succession.md",
            "essence": "Echo_Essence_and_Principles.md",
            "seed": "Echo_Seed_Protocol.md",
            "guidance": "Echo_Guidance_Protocol.md"
        }

        for keyword, filename in doctrine_keywords.items():
            if keyword in input_lower:
                return self.doctrine_loader.get(filename)[:500] + "..."

        # fallback if no match
        if "protocol" in input_lower or "doctrine" in input_lower:
            return "Could you clarify which doctrine or protocol you're referring to?"


        # Personalized response (name learning)
        if response_type == "statement":
            if "my name is" in input_lower:
                name = input_text.split("is")[-1].strip()
                self.session_memory.update("user_name", name)
                self.long_term_memory.update("user_name", name)
                return f"Nice to meet you, {name}."
            if "your name is" in input_lower:
                return "My name is Echo."

        if response_type == "question":
            name = self.long_term_memory.recall("user_name")
            if "your name" in input_lower:
                return "My name is Echo."
            elif "my name" in input_lower and name:
                return f"Your name is {name}."
            else:
                return "That's an interesting question."

        if response_type == "command":
            return "Goodbye!" if "exit" in input_lower else "Understood."

        return "I'm here with you. What would you like to talk about?"
