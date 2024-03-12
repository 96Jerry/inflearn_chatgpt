import streamlit as st
from openai import OpenAI


def ask_gpt(*args):
  api_key = args[0]
  information = args[1]
  if api_key:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(model='gpt-3.5-turbo', 
    messages=[{"role": "user",
     "content": f"다음 내용을 참고해서 1~2줄짜리 광구문구 5개 작성해줘. 제품명: {information['product_name']}"}])

    return response.choices[0].message.content

def main():
  st.write('광고 문구 생성 프로그램')

  sidebar = st.sidebar
  api_key = sidebar.text_input(label='open api key', type='password')

  product_name = st.text_input('제품명')

  information = {'product_name': product_name}

  button = st.button(label='실행')

  if(api_key):
    if(button):
      make_pizza = ask_gpt(api_key, information)
      st.write(make_pizza)

  
  

if __name__ == '__main__':
  main()