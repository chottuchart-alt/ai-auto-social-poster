import os
import requests
from openai import OpenAI

# ENV VARIABLES
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_ORG_ID = os.getenv("LINKEDIN_ORG_ID")
OPENAI_KEY = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=OPENAI_KEY)

def generate_content():
    prompt = """
    Create a powerful LinkedIn post promoting an AI automation service.
    Make it professional, engaging and include 3 hashtags.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def post_to_linkedin(content):
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
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)

if __name__ == "__main__":
    content = generate_content()
    post_to_linkedin(content)
