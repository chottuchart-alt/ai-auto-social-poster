import requests
from openai import OpenAI
import os

# ===== ENV VARIABLES =====
OPENAI_KEY = os.getenv("OPENAI_KEY")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_ORG_ID = os.getenv("LINKEDIN_ORG_ID")

# ===== AI CONTENT =====
client = OpenAI(api_key=OPENAI_KEY)

def generate_caption():
    prompt = """
    Write a professional LinkedIn post promoting a Gold Trading AI Bot.
    Keep it confident, clean, and corporate.
    Add 5 finance hashtags at end.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ===== LINKEDIN POST =====
def post_linkedin(caption):

    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    data = {
        "author": f"urn:li:organization:{LINKEDIN_ORG_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": caption
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)


# ===== MAIN =====
def run():
    caption = generate_caption()
    post_linkedin(caption)


if __name__ == "__main__":
    run()
