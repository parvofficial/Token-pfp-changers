import os
import random
import requests
import base64
from io import BytesIO
from PIL import Image

# Define paths
token_file = 'data/input.txt'
avatar_links_file = 'data/avatar_links.txt'  # File containing avatar image URLs

# Read the token from the input.txt file
def read_token():
    with open(token_file, 'r') as f:
        token = f.readline().strip()
    return token

# Download the image from a URL and convert it to base64
def get_avatar_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Open the image as a PIL image object
        img = Image.open(BytesIO(response.content))
        
        # Ensure the image is in PNG format
        img = img.convert("RGBA")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        
        # Convert image to base64
        avatar_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{avatar_base64}"
    else:
        raise Exception(f"Failed to download image from {url}. Status code: {response.status_code}")

# Choose a random URL from the avatar_links.txt file
def get_random_avatar_url():
    with open(avatar_links_file, 'r') as f:
        avatar_urls = f.readlines()
    
    random_url = random.choice(avatar_urls).strip()
    return random_url

# Update the Discord avatar
def update_avatar(token, avatar_data):
    url = 'https://discord.com/api/v9/users/@me'
    headers = {
        'Authorization': f'Bot {token}',
        'Content-Type': 'application/json'
    }
    
    json_data = {
        'avatar': avatar_data
    }
    
    response = requests.patch(url, headers=headers, json=json_data)
    
    if response.status_code == 200:
        print("Avatar updated successfully!")
    else:
        print(f"Failed to update avatar: {response.status_code}, {response.text}")

def main():
    # Step 1: Read token from file
    token = read_token()
    
    # Step 2: Pick a random avatar URL from file
    random_avatar_url = get_random_avatar_url()
    
    # Step 3: Download the image and convert to base64
    random_avatar_base64 = get_avatar_from_url(random_avatar_url)
    
    # Step 4: Update avatar
    update_avatar(token, random_avatar_base64)

if __name__ == "__main__":
    main()
