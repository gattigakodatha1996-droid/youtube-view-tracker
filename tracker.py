import os
import requests
from supabase import create_client

# Load the keys you put in GitHub Secrets
YT_KEY = os.environ.get("YT_KEY")
SB_URL = os.environ.get("SB_URL")
SB_KEY = os.environ.get("SB_KEY")

supabase = create_client(SB_URL, SB_KEY)

# 1. Get the list of videos we want to track from our DB
response = supabase.table("videos").select("*").execute()
video_list = response.data

for video in video_list:
    yt_id = video['youtube_id']
    
    # 2. Ask YouTube for the view count
    url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={yt_id}&key={YT_KEY}"
    data = requests.get(url).json()
    
    views = data['items'][0]['statistics']['viewCount']
    
    # 3. Save that number into our 'snapshots' table
    supabase.table("snapshots").insert({
        "video_id": video['id'],
        "views": int(views)
    }).execute()

print("Daily check complete!")
