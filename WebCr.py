import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set the API credentials (replace with your own values)
API_KEY = "AIzaSyCrf1189TcvB-ILZkQQcaqx3sbiwJONOZk"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Set the search query
q = "site:youtube.com openinapp.co"

# Set the maximum number of search results to retrieve
max_results = 10000

# Create a function to retrieve the YouTube channels from the search results
def get_channels(api_key, query, max_results):
    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=api_key)
    channels = []
    next_page_token = None

    # Loop through all search result pages until max_results is reached
    while len(channels) < max_results:
        # Make a request to the search.list method to retrieve the search results
        search_response = youtube.search().list(
            q=query,
            type="channel",
            pageToken=next_page_token,
            part="id,snippet",
            maxResults=min(max_results - len(channels), 50)
        ).execute()

        # Loop through each search result and extract the channel information
        for search_result in search_response.get("items", []):
            channel_id = search_result["id"]["channelId"]
            channel_title = search_result["snippet"]["title"]
            channel_description = search_result["snippet"]["description"]
            channel_url = f"https://www.youtube.com/channel/{channel_id}"
            channels.append({
                "channel_id": channel_id,
                "channel_title": channel_title,
                "channel_description": channel_description,
                "channel_url": channel_url
            })

        # Check if there are more search result pages
        next_page_token = search_response.get("nextPageToken")
        if not next_page_token:
            break

    return channels

# Call the get_channels function to retrieve the YouTube channels from the search results
try:
    channels = get_channels(API_KEY, q, max_results)
except HttpError as e:
    print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
    channels = []

# Save the channels to a CSV file
if channels:
    with open("channels.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["channel_id", "channel_title", "channel_description", "channel_url"])
        writer.writeheader()
        writer.writerows(channels)
    print(f"Found {len(channels)} channels and saved to channels.csv")
else:
    print("No channels found")
