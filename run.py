# This is a test runner to test locally
import json

from myq import lambda_handler
from myq import MODE_TEST, MODE_NONTEST
from myq import ACTION_OPEN, ACTION_CLOSE

class Context:
    def __init__(self, arn: str):
        self.invoked_function_arn = arn


if __name__ == "__main__":
    event = {"action": ACTION_CLOSE, "mode": MODE_TEST}
    response = lambda_handler(event, Context("Sample ARN"))
    print(response)