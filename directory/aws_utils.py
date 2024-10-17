import boto3
from django.conf import settings
import time

def upload_audio_to_s3(file_path, bucket_name, s3_file_key):
    """
    Upload the audio file to an S3 bucket.
    """
    s3 = boto3.client('s3', 
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_REGION)
    s3.upload_file(file_path, bucket_name, s3_file_key)
    return f"s3://{bucket_name}/{s3_file_key}"

def start_transcription_job(s3_url, job_name):
    """
    Start an AWS Transcribe job on an audio file stored in S3.
    """
    transcribe = boto3.client('transcribe', 
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                              region_name=settings.AWS_REGION)

    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3_url},
        MediaFormat='mp3',  # Adjust based on your format
        LanguageCode='en-US'  # Change this for your desired language
    )
    
    return response['TranscriptionJob']['TranscriptionJobName']

def get_transcription_result(job_name):
    """
    Retrieve the transcript after the job is completed.
    """
    transcribe = boto3.client('transcribe', 
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                              region_name=settings.AWS_REGION)

    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = response['TranscriptionJob']['TranscriptionJobStatus']
        if status in ['COMPLETED', 'FAILED']:
            break
        time.sleep(30)
    
    if status == 'COMPLETED':
        return response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    else:
        raise Exception('Transcription job failed.')
