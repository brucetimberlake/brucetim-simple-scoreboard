from pathlib import Path
import boto3

# Load the template located in the same directory as this file.
template_html = (Path(__file__).parent / "template.html").read_text()

# Connect to DynamoDB.
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("brucetim-simple-scoreboard")

def lambda_handler(event, context):
    # Display the scores in table format.
    scores = "\n".join(
        [
            f"<tr><td>{item['name']}</td><td>{item['score']}</td></tr>"
            for item in table.scan()["Items"]
        ]
    )

    response = {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": template_html.format(scores=scores),
    }
    return response
