import os
import googleapiclient.discovery
import csv

API_KEY = "AIzaSyAnG1ymMRrt4L-6BnvtB4kYaEmtmT3K7Pk"

def get_youtube_service():
    return googleapiclient.discovery.build(
        "youtube", "v3", developerKey=API_KEY
    )

def fetch_videos_by_genre_and_channel(genre, channel_ids, max_results=500):
    youtube = get_youtube_service()
    videos = []

    for channel_id in channel_ids:
        search_response = youtube.search().list(
            channelId=channel_id,
            q=genre,
            part="id,snippet",
            type="video",
            maxResults=50
        ).execute()

        for item in search_response.get("items", []):
            videos.append(item["id"]["videoId"])

        next_page_token = search_response.get("nextPageToken")
        while next_page_token and len(videos) < max_results:
            search_response = youtube.search().list(
                channelId=channel_id,
                q=genre,
                part="id,snippet",
                type="video",
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in search_response.get("items", []):
                videos.append(item["id"]["videoId"])

            next_page_token = search_response.get("nextPageToken")

        if len(videos) >= max_results:
            break

    return videos[:max_results]

def fetch_video_details(video_ids):
    youtube = get_youtube_service()
    video_details = []

    for i in range(0, len(video_ids), 50):
        response = youtube.videos().list(
            part="snippet,contentDetails,statistics", id=','.join(video_ids[i:i+50])
        ).execute()

        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            content_details = item.get("contentDetails", {})
            statistics = item.get("statistics", {})

            video_details.append({
                "Video URL": f"https://www.youtube.com/watch?v={item['id']}",
                "Title": snippet.get("title"),
                "Description": snippet.get("description"),
                "Channel Title": snippet.get("channelTitle"),
                "Keyword Tags": snippet.get("tags"),
                "Category": snippet.get("categoryId"),
                "Published At": snippet.get("publishedAt"),
                "Duration": content_details.get("duration"),
                "View Count": statistics.get("viewCount"),
                "Comment Count": statistics.get("commentCount"),
                "Captions Available": "true" if "caption" in content_details else "false"
            })

    return video_details

def save_to_csv(data, filename="youtube_videos.csv"):
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def main():
    genre = "Action"
    channel_ids = input("Enter the channel IDs separated by commas: ").split(',')
    print("Fetching videos for genre:", genre)

    video_ids = fetch_videos_by_genre_and_channel(genre, channel_ids)
    print(f"Fetched {len(video_ids)} video IDs.")

    video_details = fetch_video_details(video_ids)
    print(f"Fetched details for {len(video_details)} videos.")

    save_to_csv(video_details)
    print("Data saved to youtube_videos.csv")

if __name__ == "__main__":
    main()
