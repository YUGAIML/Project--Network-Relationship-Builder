import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

def get_channel_statistics(channel_id):

    request = youtube.channels().list(
        part="statistics",
        id=channel_id
    )

    response = request.execute()

    if not response["items"]:
        return {
            "subscribers": "N/A",
            "videos": "N/A",
            "views": "N/A"
        }

    stats = response["items"][0]["statistics"]

    return {

        "subscribers": stats.get("subscriberCount", "N/A"),

        "videos": stats.get("videoCount", "N/A"),

        "views": stats.get("viewCount", "N/A")

    }



def recommend_channels(skills):

    query = " ".join(skills)

    request = youtube.search().list(
        part="snippet",
        q=query,
        type="channel",
        maxResults=10
    )

    response = request.execute()

    channels = []

    for item in response["items"]:

        channel_id = item["snippet"]["channelId"]

        stats = get_channel_statistics(channel_id)

        channels.append({

            "title": item["snippet"]["title"],

            "description": item["snippet"]["description"],

            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],

            "channel_id": channel_id,

            "url": f"https://www.youtube.com/channel/{channel_id}",

            "subscribers": stats["subscribers"],

            "videos": stats["videos"],

            "views": stats["views"]

        })

    return channels

def search_videos(skills):

    query = " ".join(skills)

    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=8
    )

    response = request.execute()

    videos = []

    for item in response.get("items", []):

        video_id = item["id"].get("videoId")

        if not video_id:
            continue

        videos.append({

            "title": item["snippet"]["title"],

            "description": item["snippet"]["description"],

            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],

            "channel": item["snippet"]["channelTitle"],

            "published": item["snippet"]["publishedAt"][:10],

            "url": f"https://www.youtube.com/watch?v={video_id}"

        })

    return videos