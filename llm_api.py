import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
import os
import pathlib
import warnings

load_dotenv()

warnings.filterwarnings("ignore", category=DeprecationWarning)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

def text_generator(user_prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_prompt)
    return response.text

# def text_generator(user_prompt):
#     model = genai.GenerativeModel("gemini-pro")
#     chat = model.start_chat(history=[])
#     response = chat.send_message(user_prompt)
#     return chat.history
 
def caption_generator(user_prompt, image):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([user_prompt, image])
    response.resolve()
    return response.text

def video_summary_generator(transcript_text):
    model=genai.GenerativeModel("gemini-pro")
    prompt="""
    You are a highly advanced AI language model, and you have been provided with the transcriptions of a YouTube video. Your task is to generate a detailed summary of the video contents, ensuring that no crucial information is omitted. After the summary, you are required to identify and explain important technical terms and/or concepts discussed in the video. Use your extensive knowledge to provide an in-depth understanding of the content covered.
    #INSTRUCTIONS:
    1. Provide a comprehensive summary of the video content, covering key points and details.
    2. Identify and explain any technical terms or concepts introduced in the video.
    3. Use your own knowledge to elaborate on the video content and provide additional insights or context.
    #NOTE: If the video covers a specific field or topic, make sure to draw on relevant knowledge to enhance the summary and explanations.
    Here is the YouTube video transcription: 
    """
    response=model.generate_content(prompt+transcript_text)
    return response.text 

def image_generator(user_prompt):
    response = client.images.generate(
    model="dall-e-3",
    prompt="I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: "+user_prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )
    image_url = response.data[0].url
    return image_url

def audio_to_text(file):
    audio_file= open(file, "rb")
    translation = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file,
    )
    return translation.text

def text_to_audio(text):
    speech_file_path = "ai_speech.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text
    )

    response.stream_to_file(speech_file_path)
    
def generate_summary(text):
    prompt = "Given a PDF document text, generate a concise and informative summary that captures the key ideas, main arguments, and relevant details. Ensure the summary is well-organized and coherent, providing a clear overview of the document's content: "+text
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )
    return response.choices[0].message.content