import requests
from PIL import Image, ImageDraw
from openai import OpenAI
import os
import base64
import time

# ====== ENV VARIABLES ======
OPENAI_KEY = os.getenv("OPENAI_KEY")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")
IG_USER_ID = os.getenv("IG_USER_ID")

# ====== AI CONTENT ======
client = OpenAI(api_key=OPENAI_KEY)

def generate_caption():
    prompt = """
    Create a powerful professional promotional post for a Gold Trading AI Bot.
    Include:
    - Strong hook
    - Authority tone
    - CTA
    - 6 finance hashtags
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ====== CREATE IMAGE ======
def create_image():
    img = Image.new("RGB", (1080, 1080), "black")
    draw = ImageDraw.Draw(img)
    draw.text((200, 500), "🔥 GOLD AI BOT 🔥", fill="gold")
    img.save("post.png")


# ====== UPLOAD IMAGE TO FACEBOOK ======
def upload_photo_facebook(caption):

    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/photos"

    files = {
        "source": open("post.png", "rb")
    }

    payload = {
        "caption": caption,
        "access_token": META_ACCESS_TOKEN
    }

    response = requests.post(url, data=payload, files=files)
    print("Facebook:", response.text)


# ====== INSTAGRAM POST ======
def post_instagram(caption):

    # STEP 1: Upload image container
    upload_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media"

    payload = {
        "image_url": f"https://graph.facebook.com/v18.0/{PAGE_ID}/picture?access_token={META_ACCESS_TOKEN}",
        "caption": caption,
        "access_token": META_ACCESS_TOKEN
    }

    container = requests.post(upload_url, data=payload)
    container_data = container.json()

    if "id" not in container_data:
        print("Instagram container error:", container.text)
        return

    creation_id = container_data["id"]

    time.sleep(5)

    # STEP 2: Publish
    publish_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media_publish"

    publish_payload = {
        "creation_id": creation_id,
        "access_token": META_ACCESS_TOKEN
    }

    response = requests.post(publish_url, data=publish_payload)
    print("Instagram:", response.text)


# ====== MAIN ======
def run():
    caption = generate_caption()
    create_image()

    upload_photo_facebook(caption)
    time.sleep(5)
    post_instagram(caption)


if __name__ == "__main__":
    run()

