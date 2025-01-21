import requests
import pandas as pd

# Spotify API credentials
CLIENT_ID = "YOUR CLIENT ID"  # Masukkan Client ID Anda
CLIENT_SECRET = "YOUR CLIENT SECRET"  # Masukkan Client Secret Anda

# You can get the CLIENT ID and CLIENT SECRET on www.developer.spotify.com

# Step 1: Authenticate and get token
def get_spotify_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to authenticate: {response.json()}")

# Step 2: Search for album cover
def get_album_cover_url(track_name, artist_name, token):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": f"track:{track_name} artist:{artist_name}",
        "type": "track",
        "limit": 1
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        items = response.json().get("tracks", {}).get("items", [])
        if items:
            return items[0]["album"]["images"][0]["url"]  # URL of the album cover
        else:
            return None  # No album found
    else:
        raise Exception(f"Failed to search for track: {response.json()}")

# Step 3: Add album cover URL to dataset
def add_album_cover_urls(data, token):
    data["Album Cover URL"] = data.apply(
        lambda row: get_album_cover_url(row["Track"], row["Artist"], token), axis=1
    )
    return data

# Main script
if __name__ == "__main__":
    # Load dataset
    file_path = r"C:\Users\Vicky\Downloads\most streamed spotify songs 2024\Most Streamed Spotify Songs 2024.csv"
  # Replace with your file path
    spotify_data = pd.read_csv(file_path, encoding='ISO-8859-1')

    # Get Spotify token
    token = get_spotify_token(CLIENT_ID, CLIENT_SECRET)

    # Add album cover URLs
    enriched_data = add_album_cover_urls(spotify_data, token)

    # Save the updated dataset
    enriched_file_path = file_path
    enriched_data.to_csv(enriched_file_path, index=False)

    print(f"Dataset updated with album cover URLs saved to {enriched_file_path}")

import pandas as pd

df = pd.read_csv("C:\\Users\\Vicky\\Downloads\\most streamed spotify songs 2024\\Most Streamed Spotify Songs 2024.csv")
print(df.head())