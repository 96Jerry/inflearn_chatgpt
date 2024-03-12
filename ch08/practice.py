import os

import openai
import requests
import streamlit as st
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate
from instagrapi import Client
from PIL import Image

load_dotenv(verbose=True)

user_api_key = st.text_input(label='openai api key', type="password")

def ask_gpt_chat(prompt, user_api_key):
  client = openai.OpenAI(api_key=user_api_key)
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
  )
  getResponse = response.choices[0].message.content

  return getResponse

def ask_gpt_image(prompt, user_api_key):
  client = openai.OpenAI(api_key=user_api_key)
  response = client.images.generate(
    model='dall-e-2',
    prompt=prompt,
    size="256x256",
    quality="standard",
    n=1
  )
  getResponse = response.data[0].url

  return getResponse

def google_translate(text, target):
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)

    return result['translatedText']



subject_input = st.text_input(label='주제')
mood_input = st.text_input(label='분위기(e.g. 재미있는)')

en_translated_subject_input = google_translate(subject_input,'en')
prompt_text = f"tell me instagram post content with using hashtags about situation that subject : {en_translated_subject_input}, mood: {mood_input}"

en_translated_mood_input = google_translate(mood_input,'en')
prompt_image = f"draw me some image with subject : {subject_input}, mood: {en_translated_mood_input} in general drawing style"

if st.button('chat 실행'):
  en_chat_result = ask_gpt_chat(prompt_text, user_api_key)
  st.write(google_translate(en_chat_result,'ko'))

if st.button('image 실행'):
  # im = Image.open(requests.get(url=ask_gpt_image(prompt_image, user_api_key), stream=True).raw)
  # im.show()
  st.markdown(body="![Image Description]({})".format(ask_gpt_image(prompt_image, user_api_key)))


if st.button('번역'):
  st.write(google_translate(text='hello my friend',target='ko'))

if st.button('인스타 올리기'):
  cl = Client()

  
  ACCOUNT_USERNAME = os.getenv('ACCOUNT_USERNAME')
  ACCOUNT_PASSWORD = os.getenv('ACCOUNT_PASSWORD')
  cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

  media = cl.photo_upload(
    '/Users/paradise/Downloads/dog.jpeg',
    "Test caption for photo with #hashtags and mention users such @example",
    extra_data={
        "custom_accessibility_caption": "alt text example",
        "like_and_view_counts_disabled": 1,
        "disable_comments": 1,
    }
)
