from screenCapture import screenCapture
from google import genai
from dotenv import load_dotenv
from google.genai import types
import os
import pyautogui as auto

load_dotenv()

#prompt
def prompt():

    msg = f'Calculate the X and Y co-ordinate of the mouse from where it is intially to reach the input box of chatgpt relative to the screen {auto.size()}'
    return msg

#llm generates a checklist and follows it
def reason():
    client = genai.Client(api_key=os.environ.get("API_KEY"))
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            types.Part.from_bytes(
                data=screenCapture(),
                mime_type='image/png'
            ),
            prompt()
        ]
    )

    return(response.text)