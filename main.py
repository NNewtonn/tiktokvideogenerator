from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_audioclips, concatenate_videoclips
import requests
import json
import os
import apis
import random
from freesounddownload import sound_filename
import promptsrequest
from datetime import datetime

# API keys
API_KEY_PEXELS = apis.api_key_pexels


# Function to search for videos on Pexels
def search_videos(query, per_page):
    url = 'https://api.pexels.com/videos/search'
    headers = {
        'Authorization': API_KEY_PEXELS
    }
    params = {
        'query': query,
        'page': random.randint(1, 7),
        'per_page': per_page,
        'size': 'medium',
        'orientation': 'portrait'
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Function to download a video


def download_video(url, filepath):
    response = requests.get(url, stream=True)
    with open(filepath, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    print(f'Video downloaded: {filepath}')


# Search for videos
query = 'background ' + promptsrequest.daily_emotion
videos = search_videos(query, per_page=15)
promptsrequest.request_chatgpt()
# Download the first video in the results
print(len(videos))
if 'videos' in videos:
    random_video = random.randint(0, len(videos)-1)
    video = videos['videos'][random_video]
    print(random_video)
    video_url = video['video_files'][random_video]['link']
    video_filename = os.path.join('downloads', f"{video['id']}.mp4")

    # Create downloads directory if it doesn't exist
    os.makedirs(os.path.dirname(video_filename), exist_ok=True)

    # Download the video
    download_video(video_url, video_filename)

    # Edit
    # Load the video
    video_clip = VideoFileClip(video_filename)
    # Duration of the video
    video_duration = video_clip.duration
    print("Video duration")
    print(video_duration)
    # Trim the video to 30 seconds if longer
    video_clip = video_clip.subclip(0, min(30, video_duration))

    # Load the audio
    audio_clip = AudioFileClip(sound_filename)

    # Calculate how many times to repeat the audio to match the video duration
    print("Audio duration before")

    print(audio_clip.duration)
    audio_duration = audio_clip.duration
    audio_repeats = int((30 / video_clip.duration) / audio_duration) + 1
    print("Audio duration")

    print(audio_duration)

    # If video duration is less than 30 seconds, concatenate enough times to reach 30 seconds
    if video_duration < 30:
        repeats_needed = int(30 / video_duration) + 1
        final_clip = concatenate_videoclips([video_clip] * repeats_needed)
        print(concatenate_videoclips)
    # Loop the audio to match the video duration
    if (audio_duration < video_duration):
        audio_clips = [audio_clip] * audio_repeats
        final_audio_clip = concatenate_audioclips(audio_clips)

    # Trim audio to match the video duration
    final_audio_clip = audio_clip.subclip(0, video_clip.duration)

    # Set the audio to the video
    final_clip = video_clip.set_audio(final_audio_clip)

    # Get the current date and time
    current_datetime = datetime.now()

    # Format the current date and time as a single string of numbers
    datetime_string = current_datetime.strftime('%Y%m%d%H%M%S')
    # Write the final video to a file
    # Check if the folder exists
    if not os.path.exists("finished_videos"):
        # If the folder does not exist, create it
        os.makedirs("finished_videos")
        print("Folder finished_videos created.")
    else:
        print("Folder finished_videos already exists.")

    final_clip.write_videofile(
        "finished_videos/final_output" + datetime_string + ".mp4", fps=30)
else:
    print('No videos found')
