import sys
import os
from getpass import getpass

from cloudflare import Cloudflare

# Initialize client
client = Cloudflare(api_token="wvzu3Qmn1F6_kVYFittG_W6lS8KU-YrziZ13qeX7")

def prompt_user(message):
    # Load wardrobe
    # walk through the 'Clothes' directory and load allthe file names
    wardrobe = os.listdir('./Clothes')
    clothes = []
    for i, item in enumerate(wardrobe):
        clothes.append(item.split('.')[0])
    
    return client.workers.ai.run(
    "@cf/meta/llama-3.1-70b-instruct" ,
    account_id="8092ff09793e43cc8e1c906cfa5af408",
    messages=[
        {"role": "system", "content": """
            You are a fashion advisor"""
        },
        {"role": "assistant", "content":f'Assume the clothes that my wardrobe contains is the following: {", ".join(clothes)}. Respond only with a list of the clothes that would be appropriate for the occasion in CSV format.'},
        {"role": "user", "content": message}
    ]
    )

if __name__ == '__main__':
    for i in range(100):
        result = prompt_user("What should I wear to a date?")
        
        print(result["response"])