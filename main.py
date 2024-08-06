from src.arxiv_tracker import ArxivTracker


def run_daily_task():
    tracker = ArxivTracker()
    tracker.run()


if __name__ == "__main__":
    run_daily_task()
