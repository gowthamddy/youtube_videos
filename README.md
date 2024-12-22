# Data Scraping of Youtube Videos for an Action Genre

## Objective
Gather data from YouTube Videos including Video Captions using YouTube APIs or build a scraper.

## Steps:-

### API Key Retrival

1. go to "https://console.cloud.google.com/apis/api/youtube.googleapis.com"
2. Click on **Credentials**
3. Create an API Key
4. View API Key
5. Copy API Key

### Steps to Run Code

1. Install Libraries googleapiclient, csv using below PIP command
2. python -m  pip install --upgrade google-api-python-client
3. In parallel choose a GENRE for retriving Youtube data.
4. In my case, I have choosen "Action" Genre from T-Series Channel.
5. Copy Youtube channel link and go to "https://commentpicker.com" and paste it and retrive **Channel ID**
6. Now Paste your API Key retrived from **API Key Retrival** in get_youtube_service() function
7. Run python **main.py** and paste **Channel ID**
8. We get **Youtube_videos.csv**




