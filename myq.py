
def lambda_function(event, context):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return {
        'statusCode': 200,
        'body': "Tthe time is: " + current_date
    }