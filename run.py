# This is a test runner to test locally
import json

from myq import lambda_handler
from myq import MODE_TEST, MODE_NONTEST
from myq import ACTION_OPEN, ACTION_CLOSE

class Context:
    def __init__(self, arn: str):
        self.invoked_function_arn = arn


if __name__ == "__main__":
    # action=close&mode=nontest_mode&pin=3338
    event = {"body": "YWN0aW9uPWNsb3NlJm1vZGU9bm9udGVzdF9tb2RlJnBpbj0zMzM4"}
    response = lambda_handler(event, Context("Sample ARN"))
    print(response)