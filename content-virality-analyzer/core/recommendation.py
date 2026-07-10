from core.data_loader import DataLoader


class RecommendationEngine:

    def __init__(self):
        loader = DataLoader()

        self.hashtags = loader.load_hashtags()
        self.audio = loader.load_audio()

    def generate(self, analysis):

        insights = []
        recommendations = []
        content_type = analysis["content_type"]

        if analysis["content_score"] >= 24:
            insights.append("The selected content type has good engagement potential")
        else:
            insights.append("The selected content type has moderate engagement potential")


        hashtag_info = analysis["hashtag_analysis"]
        if len(hashtag_info["matching_count"]) > 0:
            insights.append(f"{len(hashtag_info['matching_count'])} hashtag(s) closely match the selected content")

        if len(hashtag_info["general_count"]) > 0:
            insights.append(f"{len(hashtag_info['general_count'])} general hashtag(s) detected")

        if len(hashtag_info["less_relevant_count"]) > 0:
            suggested = (
                self.hashtags[
                    self.hashtags["recommended_for"].str.lower()
                    == content_type.lower()
                ]
                .sort_values("points", ascending=False)
                .head(5)["hashtag"]
                .tolist()
            )

            recommendations.append({
                "type": "hashtags",
                "title": "Consider using hashtags more closely related to your content",
                "suggestions": suggested,
                "reason":"Some hashtags are less relevant to the selected content category"
            })

        if len(hashtag_info["unknown_count"]) > 0:
            insights.append(f"{len(hashtag_info['unknown_count'])} hashtag(s) are not found in the dataset")


        if analysis["audio_score"] >= 15:
            insights.append("The selected audio is on trend")
        else:
            insights.append("The selected audio has moderate trend popularity")
            suggested_audio = (
                self.audio[
                    self.audio["recommended_for"].str.lower()
                    == content_type.lower()
                ]
                .sort_values("points", ascending=False)
                .head(3)["audio_name"]
                .tolist()
            )

            if not suggested_audio:
                suggested_audio = (
                    self.audio
                    .sort_values("points", ascending=False)
                    .head(3)["audio_name"]
                    .tolist()
                )

            recommendations.append({
                "type": "audio",
                "title":"Consider using a trending audio",
                "suggestions":suggested_audio,
                "reason":"Trending audio receives more views"
            })



        if analysis["length_score"] == 15:
            insights.append("The video length is within the recommended range")

        else:
            recommendations.append({
                "type": "length",
                "title":"Consider adjusting the video length",
                "suggestions":["15–30 seconds"],
                "reason":"People most likely to watch video that's in between 15 to 30 seconds long"
            })



        if analysis["time_score"] == 15:
            insights.append("The selected posting time is in peak engagement period")

        else:
            recommendations.append({
                "type": "time",
                "title":"Consider posting during a peak engagement period",
                "suggestions":["12:00–14:00", "17:00–22:00"],
                "reason":"People mostly spend their time on screen after meals or work hour"
            })

        return {
            "insights": insights,
            "recommendations": recommendations
        }