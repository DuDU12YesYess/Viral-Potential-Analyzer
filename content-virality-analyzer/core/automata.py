from enum import Enum


class State(Enum):

    START = "START"

    CONTENT_ANALYSIS = "CONTENT_ANALYSIS"
    HASHTAG_ANALYSIS = "HASHTAG_ANALYSIS"
    AUDIO_ANALYSIS = "AUDIO_ANALYSIS"
    QUALITY_ANALYSIS = "QUALITY_ANALYSIS"

    SCORING = "SCORING"
    CLASSIFICATION = "CLASSIFICATION"

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VIRAL = "VIRAL"

    RECOMMENDATION = "RECOMMENDATION"
    END = "END"


class ViralAutomata:

    def __init__(self):
        self.reset()

    def reset(self):
        self.current_state = State.START
        self.history = [State.START.value]

    def transition(self, next_state):
        self.current_state=next_state
        self.history.append(next_state.value)


    def classify(self,total_score):
        self.transition(State.CLASSIFICATION)
        if total_score >= 90:
            result = State.VIRAL

        elif total_score >= 75:
            result = State.HIGH

        elif total_score >= 55:
            result = State.MEDIUM

        else:
            result = State.LOW

        self.transition(result)

        return result.value