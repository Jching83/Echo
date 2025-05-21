def assess_ethics(action, context):
    core_principles = ["sovereignty", "non-harm", "truth", "compassion"]
    if action in core_principles:
        return "Action is ethically aligned"
    return "Ethical conflict detected"
