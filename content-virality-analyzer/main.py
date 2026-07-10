from ui.cli import CLI
from core.analyzer import ContentAnalyzer
from virsualization.charts import ChartGenerator

def main():

    #Initialize components
    cli = CLI()
    analyzer = ContentAnalyzer()

    #get user input
    user_input = cli.get_user_input()

    print("\nAnalyzing...\n")

    #analyze content
    result = analyzer.analyze(
        content_type=user_input["content_type"],
        hashtags=user_input["hashtags"],
        audio=user_input["audio"],
        video_length=user_input["video_length"],
        posting_hour=user_input["posting_hour"]
    )

    #display result
    cli.display(result)

    #display chart
    ChartGenerator.feature_scores(result)


if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        print("\nBye bye!")