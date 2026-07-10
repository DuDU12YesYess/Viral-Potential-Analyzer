import matplotlib.pyplot as plt


class ChartGenerator:

    @staticmethod
    def feature_scores(result):

        labels = [
            "Content",
            "Hashtags",
            "Audio",
            "Length",
            "Time"
        ]

        scores = [
            result["content_score"],
            result["hashtag_score"],
            result["audio_score"],
            result["length_score"],
            result["time_score"]
        ]

        plt.figure(figsize=(8,5))
        plt.bar(labels, scores)

        plt.title("Feature Score Comparison")
        plt.xlabel("Features")
        plt.ylabel("Points")

        plt.ylim(0, 25)

        # plt.tight_layout()
        plt.show()