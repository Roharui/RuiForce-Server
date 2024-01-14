import os

from dotenv import load_dotenv

from consumer.goal_consumer import GoalConsumer

load_dotenv()

ENV = {**os.environ}

if __name__ == "__main__":
    try:
        consumer = GoalConsumer(ENV)
        consumer.main()
    except KeyboardInterrupt:
        pass
