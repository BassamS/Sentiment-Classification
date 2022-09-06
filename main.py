import json
from yt_extractor import get_video_info, get_audio_url
from api import save_transcript


def save_video_sentiments(url):
    video_info = get_video_info(url)
    audio_url = get_audio_url(video_info)
    title = video_info["title"]
    title = title.strip().replace(" ", "_")
    title = "data/" + title
    save_transcript(audio_url, title, sentiment_analysis=True)


if __name__ == "__main__":
    save_video_sentiments("https://www.youtube.com/watch?v=e-kSGNzu0hM")
