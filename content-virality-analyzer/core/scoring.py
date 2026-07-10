
class Scoring: 
    def __init__(self, content,hashtag,audio,length,time):
        self.content= content
        self.hashtag= hashtag
        self.audio= audio
        self.length= length
        self.time= time

    def score_content_type (self,content_type):
        row = self.content[
            self.content["content_type"].str.lower() == content_type.lower()
        ]

        if not row.empty: 
            return int(row["points"].iloc[0])
        return 0
    
    def _get_content_category(self, content_type):
        row = self.content[
            self.content["content_type"].str.lower() == content_type.lower()
        ]
        if not row.empty:
            return str(row["category"].iloc[0]).lower()
        return None
    
    def score_hashtags(self, hashtags, content_type):
        matching_count = []
        general_count = []
        less_relevant_count = []
        unknown_count = []

        total = 0
        content_category = self._get_content_category(content_type)
        hashtags = list(set(hashtags))  # avoid duplicates

        for tag in hashtags:
            tag = tag.strip().lower()

            row = self.hashtag[
                self.hashtag["hashtag"].str.lower() == tag
            ]

            # Not found in dataset
            if row.empty:
                unknown_count.append(tag)
                continue

            hashtag_category = str(row["category"].iloc[0]).lower()
            points = int(row["points"].iloc[0])

            if hashtag_category == "general":
                general_count.append(tag)
                total += points

            elif hashtag_category == content_category:
                matching_count.append(tag)
                total += points

            else:
                less_relevant_count.append(tag)

        return total, {
            "matching_count": matching_count,
            "general_count": general_count,
            "less_relevant_count": less_relevant_count,
            "unknown_count": unknown_count
        }
    
    def score_audio(self,audio):
        row = self.audio[
            self.audio["audio_name"].str.lower() == audio.lower()
        ]

        if not row.empty: 
            return int(row["points"].iloc[0])
        return 0
    
    def score_video_length(self,seconds):
        for _, row in self.length.iterrows():
            min_sec = row ["min"]
            max_sec = row ["max"]

            if min_sec <= seconds <= max_sec:
                return int(row["points"])
        return 0
    
    def score_posting_time(self, hour):
        for _, row in self.time.iterrows():
            start = row ["start"]
            end = row ["end"]

            if start <= hour < end:
                return int(row["points"])
        return 0
