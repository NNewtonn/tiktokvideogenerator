import requests
import os
import apis
import promptsrequest
import random

# API keys
API_KEY = apis.api_key_freesound

# Function to search for sounds on Freesound
def search_sounds(query, num_results=1):
    url = 'https://freesound.org/apiv2/search/text/'
    headers = {
        'Authorization': f'Token {API_KEY}'
    }
    params = {
        'query': query,
        'fields': 'id,name,previews',
        'page_size': num_results,
        'duration' : 36
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Function to download a sound
def download_sound(sound_url, filepath):
    response = requests.get(sound_url, stream=True)
    with open(filepath, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    print(f'Sound downloaded: {filepath}')

# Search for sounds
query = 'background music ' + promptsrequest.daily_emotion
sounds = search_sounds(query, num_results=1)

# Download the first sound in the results
quantity_sounds = len(sounds['results'])
if 'results' in sounds and quantity_sounds > 0:
    sound = sounds['results'][random.randint(0, quantity_sounds-1)]
    sound_url = sound['previews']['preview-lq-mp3']
    sound_filename = os.path.join('downloads', f"{sound['id']}_{sound['name']}.mp3")
    
    # Create downloads directory if it doesn't exist
    os.makedirs(os.path.dirname(sound_filename), exist_ok=True)
    
    # Download the sound
    download_sound(sound_url, sound_filename)
else:
    print('No sounds found')
