import sys
import os
from getpass import getpass

from cloudflare import Cloudflare
from IPython.display import display, Image, Markdown, Audio
import requests

# Initialize client
client = Cloudflare(api_token="wvzu3Qmn1F6_kVYFittG_W6lS8KU-YrziZ13qeX7")
for i in range(100):
    result = client.workers.ai.run(
    "@cf/meta/llama-3-8b-instruct" ,
    account_id="8092ff09793e43cc8e1c906cfa5af408",
    messages=[
        {"role": "system", "content": """
            You are a fashion advisor"""
        },
        {"role": "assistant", "content":"Respond in the form of [basic colour] [basic clothing item], two words please"},
        {"role": "user", "content": "What should I wear to my English literature class today?"}
    ]
    )

    display(result["response"])