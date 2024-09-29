# EchoMind: Stream of Thought to Text
[![Streamlit](https://img.shields.io/badge/streamlit-v1.36.0-brightgreen)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-LPU_Accelerated-brightgreen)](https://groq.com/)

**EchoMind** is an AI-driven voice assistant that converts your spoken thoughts into text. It integrates cutting-edge speech-to-text and language models, allowing users to dictate emails, create prompts for AI tools, and generate other kinds of text-based outputs efficiently.  
## Features
- **Speech-to-Text**: Converts spoken words into text using highly optimized transcription models.
- **Voice-Based Interaction**: Use your voice to draft emails, social media posts, or any kind of text for personal or professional workflows.
- **Model Customization**: Switch between different speech and language models depending on your needs – whether it’s speed or quality.
- **Real-Time Responses**: Ask follow-up questions or review past interactions for a fluid, voice-powered conversation experience.
- **Transcription & Inference Models**: Choose between fast and high-quality models for both speech-to-text transcription and language inference.
## How EchoMind Works
- **Press the Microphone Icon**: Record your voice.
- **Transcription**: Your speech is converted into text via state-of-the-art transcription models (powered by Groq).
- **Response Generation**: A powerful language model interprets your input and generates concise text outputs.
- **Review and Refine**: You can view past conversations, ask follow-up questions, and refine your inputs for further actions.
## Why Groq?
EchoMind leverages the Groq AI platform, which utilizes **LPUs (Linear Processing Units)**. This architecture is specially designed for handling large-scale machine learning tasks efficiently. Here's why Groq is a great fit:  
- **Blazing Speed**: Groq's LPUs process massive amounts of data in parallel, making transcription and inference incredibly fast, even for complex models.
- **Scalability**: Whether you're working with smaller models for quick tasks or larger models for intricate interactions, Groq scales seamlessly.
- **Efficiency**: LPUs offer optimized power and memory management, ensuring the platform runs smoothly even for demanding AI applications.
## Supported Models
  
  # **Speech-to-Text Models**:  
- **Distil-Whisper (Fastest)**: For lightning-fast transcription with good quality.
- **Whisper v3 (Highest Quality)**: For the highest transcription accuracy, ideal for nuanced or detailed conversations.
  
  # **Language Models**:  
- **Llama 3.2 11B (Default)**: A well-balanced model offering high-quality results.
- **Llama 3.1 70B**: For complex and extensive language understanding.
- **Llama 3.1 8B & 3B**: More lightweight models for quick responses.
- **Llama 3.2 1B (Fastest)**: The quickest model for real-time responses without compromising too much on quality.
 ## Installation
 ### Prerequisites
- Python 3.7 or above
- Install dependencies via `pip`:
  
  ```
  pip install -r requirements.txt
  ```
 ### Environment Setup
- Clone the repository.
- Create a `.env` file in the root directory and add your Groq API key:
  
  ```
  GROQ_API_KEY=your_groq_api_key_here
  ```
  Or just change the part where we get the key with your groq api key 
  ```
  os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
  ```
  
- Run the application:
  
  ```
  streamlit run app.py
  ```
  ## Usage
- Open the app in your browser.
- Press the microphone icon to start recording.
- View your transcription on the main screen and interact with the assistant.
- Choose between various models for different tasks (fast vs. high-quality transcription).
  ## Contributing
  
  Feel free to submit issues or pull requests if you'd like to contribute or suggest improvements to the project.
