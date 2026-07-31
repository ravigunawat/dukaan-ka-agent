from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY set nahi hai .env file me")
    return OpenAI(api_key=api_key)

def extract_stock_info(transcribed_text):
    client = get_client()

    prompt = f"""
Tum ek dukaan ke stock management assistant ho. Neeche diya gaya Hindi/Hinglish text ek dukandaar ne bola hai stock update ke baare me.

Text: "{transcribed_text}"

Isse ye information nikaalo aur SIRF JSON format me return karo, koi extra text nahi:
{{
  "item": "item ka naam (Hindi me jo bola gaya)",
  "quantity": number,
  "unit": "unit jaise dabba, kilo, litre, packet (agar na bola ho to null)",
  "price": number (agar bola gaya ho to, warna null),
  "action": "add" ya "remove" (stock aaya hai to add, becha/khatam hua to remove)
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    return result
