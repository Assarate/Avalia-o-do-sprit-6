import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
polly = boto3.client('polly')

def convert_to_speech(event, context):
    try:
        data = json.loads(event['body'])
        phrase = data['phrase']

        response = polly.synthesize_speech(
            OutputFormat='mp3',
            Text=phrase,
            VoiceId='Joanna'
        )

        audio_bytes = response['AudioStream'].read()

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")

        file_key = f'audio-{timestamp}.mp3'

        s3.put_object(
            Bucket='my-bucket',
            Key=file_key,
            Body=audio_bytes,
            ACL='public-read'
        )

        audio_url = f'https://my-bucket.s3.amazonaws.com/{file_key}'

        response_body = {
            "received_phrase": phrase,
            "url_to_audio": audio_url,
            "created_audio": timestamp
        }

        return {
            "statusCode": 200,
            "body": json.dumps(response_body)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
