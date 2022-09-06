from turtle import title
import requests
import time
import json
from api_secrets import API_KEY_ASSEMBLYAI


# Upload
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {'authorization': API_KEY_ASSEMBLYAI}


def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(
        upload_endpoint, headers=headers, data=read_file(filename))

    audio_url = upload_response.json()['upload_url']
    return audio_url


# Transcribe
def transcribe(audio_url, sentiment_analysis):
    transcript_request = {"audio_url": audio_url,
                          "sentiment_analysis": sentiment_analysis}
    transcript_response = requests.post(
        transcript_endpoint, json=transcript_request, headers=headers)

    job_id = transcript_response.json()['id']
    return job_id


# P0ll
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


def get_transcription_result_url(audio_url, sentiment_analysis):
    transcript_id = transcribe(audio_url, sentiment_analysis)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']

        print('Waiting 30 seconds...')
        time.sleep(30)


# Save transcription
def save_transcript(audio_url, filename, sentiment_analysis=False):
    data, error = get_transcription_result_url(audio_url, sentiment_analysis)

    if data:
        text_filename = title = ".txt"
        with open(filename, "w") as f:
            f.write(data['text'])

            if sentiment_analysis:
                filename = title + "_sentiments.json"
                with open(filename, "w") as f:
                    sentiments = data["sentiments_analysis_results"]
                    json.dump(sentiments, f, indent=4)

            print('Transcription saved!!')
    elif error:
        print("Error!!", error)
