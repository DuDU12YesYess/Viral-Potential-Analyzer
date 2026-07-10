from core.data_loader import DataLoader

class CLI:
    def __init__(self):
        loader = DataLoader()
        self.content_types = loader.load_content_types()
        self.audio = loader.load_audio()

    def get_user_input (self):
        print('='*50)
        print('CONTENT VIRAL POTENTIAL ANALYZER')
        print('='*50)

        print('\n Available Content Types: ')
        for i, content in enumerate(self.content_types["content_type"], start=1):
            print(f"{i}. {content}")

        while True:
            try: 
                choice = int(input("\nSelect Content Type (number): "))
                if 1<= choice <= len(self.content_types):
                    content_types = self.content_types.iloc[choice-1]["content_type"]
                    break

                print("Invalid Selection")
            except ValueError:
                print("Please enter a valid number :)")

        while True: 
            hashtag_input = input("\nEnter hashtags for your content: ")
            hashtags = [
                tag.strip() 
                if tag.strip().startswith("#") else f"#{tag.strip()}"
                for tag in hashtag_input.split(",")
                if tag.strip()
            ]

            hashtags = list(dict.fromkeys(hashtags)) #remove duplicate

            if len(hashtags)==0:
                print("Please, Enter your hashtags")
                continue
            if len(hashtags)>5:
                print("You can't have more than 5 hashtags in 1 content")
                continue
            break

        print("\nAvailable Audio Tracks:")
        for i, audio in enumerate(self.audio["audio_name"], start=1):
            print(f"{i}. {audio}")

        while True:
            try:
                choice = int(input("\nSelect Audio (number): "))
                if 1 <= choice <= len(self.audio):
                    audio=self.audio.iloc[choice-1]["audio_name"]
                    break
                print("Invalid Selection")
            except ValueError:
                print("Please enter a valid number :)")

        while True:
            try:
                video_length = int(input("\nVideo Length(seconds): "))
                if video_length > 0:
                    break
                print('Video length must be logner than 0s')

            except ValueError:
                print("Please enter a valid number :)")

        while True:
            try:
                posting_hour = int(input("\nPosting hour (0-23):"))
                if 0<= posting_hour <=23:
                    break
                print('Posting hour must be between 0 and 23')
            except ValueError:
                print("Please enter a valid number :)")
        return{
            "content_type": content_types,
            "hashtags": hashtags,
            "audio": audio,
            "video_length": video_length,
            "posting_hour": posting_hour
        }
    
    def display(self,result):
        print("\n" + "=" * 50)
        print("ANALYSIS RESULT")
        print("=" * 50)

        print(f"\nPrediction   : {result['prediction']}")
        print(f"Total Score  : {result['total_score']}/100")
        print("\n")

        print("-" * 30)
        print("Feature Scores")
        print("-" * 30)
        print(f"Content Type : {result['content_score']}")
        print(f"Hashtags     : {result['hashtag_score']}")
        print(f"Audio        : {result['audio_score']}")
        print(f"Video Length : {result['length_score']}")
        print(f"Posting Time : {result['time_score']}")
        print("\n")

        print("-" * 30)
        print("Automata State History")
        print("-" * 30)

        for state in result["state_history"]:
            print(state)
        print("\n")

        print("-" * 30)
        print("Insights")
        print("-" * 30)
        

        if result["insights"]:
            for insight in result["insights"]:
                print(f"✓ {insight}")
        else:
            print("No insights available.")
        print("\n")
        
        print("-" * 50)
        print("Recommendations")
        print("-" * 50)
        

        if result["recommendations"]:
            for recommendation in result["recommendations"]:
                print(f"\n => {recommendation['title']}")
                if "suggestions" in recommendation:
                    print("Suggestions:")
                    for suggestion in recommendation["suggestions"]:
                        print(f"   {suggestion}")
                print(f"Reason: {recommendation['reason']}")
        else:
            print("No recommendations. Great job!")