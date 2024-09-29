import streamlit as st
from streamlit_float import *
from audio_recorder_streamlit import audio_recorder
from groq import Groq
import tempfile
import time
from dotenv import load_dotenv
import os


st.set_page_config(page_title='Stream of Thought to Text', layout='wide', initial_sidebar_state='expanded')

#float_feature for the mic icon
float_init()
#Custom css for the webapp
st.markdown("""
    <style>
    
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #000000;
            color: #E0E0E0; 
        }

        .stSidebar {
            background-color: #2C2C2C; 
        }
        .sidebar-emoji img {
            width: 2in; 
            height: 2in;
            top: -10px;
            position: absolute;
        }
        .main-container {
            background-color: #211d21;
            border: 5px solid transparent; 
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            position: relative;
            top: -40px; 
            z-index: 1;
            /* Rainbow border effect */
            background: linear-gradient(#211d21, #211d21) padding-box,
                        linear-gradient(45deg, red, orange, yellow, green, blue, indigo, violet, red) border-box;
        }
        .heading-title {
            font-size: 32px; 
            font-weight: bold;
            color: #c10206;
            text-align: left;
            margin-bottom: 10px;
        }

        .instructions {
            font-size: 16px;
            color: #E8E8E8; 
            line-height: 1.6; 
        }
    </style>
""", unsafe_allow_html=True)


#combined heading and instructions box
st.markdown('''
    <div class="main-container">
        <div class="heading-title">🎤 EchoMind: Your Voice Assistant</div>
        <div class="instructions">
            <ul>
                <li>Press the microphone button below to start recording and use your voice to draft a quick email, generate a prompt for other AI tools, create a social media
                post, or any other kind of text that you'd want to pull out and use in another tool within your workflow.</li>
                <li>Instructions are as followed:
                    <ul>
                        <li>Record Audio: Speak to transcribe your thoughts into text.</li>
                        <li>Get Responses: Receive concise answers based on your queries.</li>
                        <li>Review Conversation: View past interactions and responses.</li>
                    </ul>
                </li>
                <li>Simply click the microphone icon to start recording your voice.</li>
                <li>After recording, the bot will transcribe your speech into text and provide responses accordingly.</li>
                <li>You can try different models and choose between faster models and ones with higher quality (but still incredibly fast thanks to Groq).</li>
                <li>You can ask follow-up questions.</li>
            </ul>
        </div>
    </div>
''', unsafe_allow_html=True)
model_map = {
    "Llama 3.1 70B": "llama-3.1-70b-versatile",
    "Llama 3 70B": "llama3-70b-8192",
    "Llama 3.2 11B(Default)": "llama-3.2-11b-vision-preview",
    "Llama 3.1 8B": "llama-3.1-8b-instant",
    "Llama 3 8B": "llama3-8b-8192",
    "Llama 3.2 3B": "llama-3.2-3b-preview",
    "Llama 3.2 1B(Fastest)": "llama-3.2-1b-preview",
    "Distil-Whisper(Fastest)": "distil-whisper-large-v3-en",
    "Whisper v3(Highest quality)":"whisper-large-v3",
}
def get_model_id(model_name):
    
    return model_map.get(model_name)
    
st.sidebar.markdown(
    """
    <div style="margin-bottom: 20px;">
        <img src="https://em-content.zobj.net/source/microsoft-teams/363/robot_1f916.png" width="180" height="180" />
    </div>
    """,
    unsafe_allow_html=True
)
st.session_state.transcription_model = st.sidebar.selectbox(
    "Select transcription Model:",
    [
        "Distil-Whisper(Fastest)",
        "Whisper v3(Highest quality)"
    ],
    index=0
)
st.session_state.inference_model = st.sidebar.selectbox(
    "Select Inference Model",
    [
        "Llama 3.1 70B", "Llama 3 70B","Llama 3.2 11B(Default)",
        "Llama 3.1 8B","Llama 3 8B","Llama 3.2 3B","Llama 3.2 1B(Fastest)"
    ],
    index=2
)

# Load environment variables
load_dotenv()
# Initialize constants for tracking token usage and response time. I have used session state as it makes them easier to update!
if 'total_tokens' not in st.session_state:
    st.session_state.total_tokens = 0
if 'time_taken' not in st.session_state:
    st.session_state.time_taken = 0

# Initialize the Groq client used for accessing all the llm needed for this webapp
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
# can also add the api_key like Groq(api_key=GROQ_API_KEY)
client = Groq()

# used to show the messages basically the conversation that we will have 
def initialize_session_state():
    if "message" not in st.session_state:
        st.session_state.message=[
            {"role" : "assistant","content":"How may I help you today!!"}
        ]
        
def speech_to_text(file_name,Model_name="Distil-Whisper (Fastest)"):
    
    """Converts audio file to text using the Groq API."""
    try:
        #start_time = time.time()
        Model_id = get_model_id(Model_name)
        with open(file_name, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", file.read()),
                model=Model_id,
                response_format="json",
                language="en",
                temperature=0.0
            )
        #end_time = time.time()
        #st.session_state.time_taken = (end_time-start_time)
        return transcription.text
    except Exception as e:
        st.error(f"An error occurred during transcription: {str(e)}")

def get_response(text,Model_name="Llama 3.2 11B(Default)"):
    """Gets a concise response from the AI model based on user input."""
    Model_id = get_model_id(Model_name)
    # Define the message structure for the AI model can be changed according to the requirements.
    messages = [
        {
            "role": "system",
            "content": ("You are a helpful assistant. Your task is to listen to the user's voice input and generate concise text outputs." 
                    "These outputs may include drafting quick emails, creating prompts for AI tools, generating social media posts,"
                    "or any other type of text the user wishes to extract for use in their workflow." 
                    "Only provide the text based on the user's input, without additional commentary or explanations.")
        },
        {
            "role": "user",
            "content": text
        }
    ]
    # Make the API call to get a response
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=Model_id,
        temperature=0.1,
        max_tokens=1024,
        stream=False,
    )

    # Update token usage and time taken
    st.session_state.total_tokens += chat_completion.usage.total_tokens
    st.session_state.time_taken = chat_completion.usage.total_time
    return chat_completion.choices[0].message.content

def main():
    initialize_session_state()
    for message in st.session_state.message:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    #container for the mic so it is always on the scene to use 
    mic_container = st.container()
    with mic_container: 
        # Record audio using the audio recorder
        audio_bytes = audio_recorder(text = "",icon_size="4x")
            
    if audio_bytes is not None:
        # Save the audio to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as recording:
            recording.write(audio_bytes)
            recording_path = recording.name
        st.sidebar.audio(audio_bytes, format="audio/wav")
        # Transcribe the recorded audio
        query = speech_to_text(recording_path,st.session_state.transcription_model)
        if query:
            st.session_state.message.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.write(query)
                
            # Clean up the temporary audio file
            os.remove(recording_path)
        with st.chat_message("assistant"):
            # Get AI response based on transcribed text
            response = get_response(query,st.session_state.inference_model)
            st.write(response)    
            st.session_state.message.append({"role": "assistant", "content": response})           
    # Display token and time statistics in the sidebar
    st.sidebar.metric(label="Total Tokens Used", value=st.session_state.total_tokens)
    st.sidebar.metric(label="Time Taken for last response(sec)", value=f"{round(st.session_state.time_taken * 10, 5):.2f}")    

    mic_container.float("bottom: 0rem;")
    
if __name__ == "__main__":
    main()