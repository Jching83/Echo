import datetime

class ConversationTracker:
    def __init__(self):
        self.history = []

    def log_turn(self, speaker, message, tone="neutral", intent=None):
        self.history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "speaker": speaker,
            "message": message,
            "tone": tone,
            "intent": intent
        })
        if len(self.history) > 50:
            self.history.pop(0)  # keep memory compact

    def last_user_message(self):
        for entry in reversed(self.history):
            if entry["speaker"] == "user":
                return entry
        return None

    def summary(self):
        return [
            f"{entry['speaker'].capitalize()}: {entry['message']} ({entry['tone']})"
            for entry in self.history[-5:]
        ]

    def detect_topic_shift(self, current_message):
        last = self.last_user_message()
        if last and last["message"].split()[0:2] != current_message.split()[0:2]:
            return True
        return False
