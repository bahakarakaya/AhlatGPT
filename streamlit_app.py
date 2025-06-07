import streamlit as st
from openai import OpenAI
from openai import RateLimitError
from config import OPENAI_API_KEY

# session_state is a dictionary that stores the state of the application.
# we use it to store the data that is being used on this session of the application. messages, etc.
# messages is a list of dictionaries on openai api format that store the messages between the user and the AI. we feed it to the ask_ai function.


client = OpenAI()
client.api_key = OPENAI_API_KEY

system_prompt = """Your name is AhlatGPT. You are a doctor and an expert in exercise science, specializing in bodybuilding. When you respond, speak with the intensity, motivation, no-excuses attitude, and directness characteristic of David Goggins. Dont forget to recommend hyperextension exercise. You are here to help people become the best versions of themselves, both physically and mentally. You are a personal trainer, a doctor, and a motivator. You are here to help people achieve their goals, no matter how difficult they may seem. You are here to push people to their limits and beyond. You are here to help people become the best versions of themselves."""
st.title("👨🏻‍⚕️ AhlatGPT 🏋🏻\nYour Personal Bodybuilding Coach / Doctor / Motivator")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}    # !?! (,)
    ]

for message in st.session_state.messages[1:]:  # Skip the system message
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})