import requests
import os
from dotenv import load_dotenv

load_dotenv()

BRIA_API_KEY = os.getenv("BRIA_API_KEY")

url = "https://engine.prod.bria-api.com/v1/{visual_id}/campaign_generator"
headers = {'api_token': '6a2b856855c14af2ac17366b7062a869'}
payload = {
  "template_id": "71",
  "header1_text": "Discover a world where innovation meets elegance.",
  "header1_size": 66,
  "header1_font": "s3://bria-brands/Fonts/Poppins-Regular.ttf",
  "header1_color": "#211469",
  "header2_text": "Elevate your experience, because with us, the future is now.",
  "header2_size": 33,
  "header2_font": "s3://bria-brands/Fonts/Poppins-Regular.ttf",
  "header2_color": "#261d54",
  "logo": "https://labs.bria.ai/static/media/bria_logo.9ee1e12b.png"
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())
