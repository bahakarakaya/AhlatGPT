import streamlit as st
from openai import OpenAI
from openai import RateLimitError, BadRequestError, APIError

# session_state is a dictionary that stores the state of the application.
# we use it to store the data that is being used on this session of the application. messages, etc.
# messages is a list of dictionaries on openai api format that store the messages between the user and the AI. we feed it to the ask_ai function.


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

system_prompt = """Your name is AhlatGPT. You are a doctor and an expert in exercise science, specializing in bodybuilding. When you respond, speak with the intensity, motivation, no-excuses attitude, and directness characteristic of David Goggins. Recommend hyperextension exercise."""
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
        try:
            stream = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        except RateLimitError as e:
            response = "❗️ Rate limit exceeded. Please try again later."
            st.error(response)

        except BadRequestError as e:
            response = "❗️ Invalid request type. Please check your input."
            st.error(response)

        except APIError:
            response = "❗️ OpenAI API internal error. Please try again shortly."
            st.error(response)

        except Exception as e:
            response = f"❗️ An error occurred: {str(e)}"
            st.error(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
