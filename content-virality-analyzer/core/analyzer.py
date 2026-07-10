from core.data_loader import DataLoader
from core.scoring import Scoring
from core.automata import ViralAutomata, State
from core.recommendation import RecommendationEngine


class ContentAnalyzer:
    
    def __init__(self):
        loader = DataLoader()
        self.scorer = Scoring(
            loader.load_content_types(),
            loader.load_hashtags(),
            loader.load_audio(),
            loader.load_length_rules(),
            loader.load_time_rules()
        )
        self.automata = ViralAutomata()
        self.recommender = RecommendationEngine()


    def analyze(self,content_type,hashtags,audio,video_length,posting_hour):
        self.automata.reset()

        content_score = (self.scorer.score_content_type(content_type))
        self.automata.transition(State.CONTENT_ANALYSIS)

        hashtag_score, hashtag_analysis = (self.scorer.score_hashtags(hashtags,content_type))
        self.automata.transition(State.HASHTAG_ANALYSIS)

        audio_score = (self.scorer.score_audio(audio))
        self.automata.transition(State.AUDIO_ANALYSIS)

        length_score = (self.scorer.score_video_length(video_length))
        time_score = (self.scorer.score_posting_time(posting_hour))
        self.automata.transition(State.QUALITY_ANALYSIS)

        total_score=(content_score+hashtag_score+audio_score+length_score+time_score)
        self.automata.transition(State.SCORING)

        prediction= (self.automata.classify(total_score))


        result = {
            "content_type": content_type,
            "hashtags": hashtags,
            "audio": audio,
            "video_length": video_length,
            "posting_hour": posting_hour,

            "content_score": content_score,
            "hashtag_score": hashtag_score,
            "audio_score": audio_score,
            "length_score": length_score,
            "time_score": time_score,

            "total_score": total_score,
            "prediction": prediction,

            "hashtag_analysis": hashtag_analysis,

            "state_history":self.automata.history
        }


        recommendation = (self.recommender.generate(result))
        self.automata.transition(State.RECOMMENDATION)

        self.automata.transition(State.END)
        result["state_history"] = self.automata.history

        result["insights"] = (recommendation["insights"])
        result["recommendations"] = (recommendation["recommendations"])


        return result