import markdown
from PIL import Image
import io
import base64
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse
import wave
import sounddevice as sd
import numpy as np
import io
from scipy.io.wavfile import write
import pydub
from PyPDF2 import PdfReader

def convert_to_markdown(text):
    return markdown.markdown(text)

def process_uploaded_image(file):
    pil_image = Image.open(file)
    return pil_image

def convert_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return encoded_image

def convert_to_video_address_link(input_link):
    parsed_url = urlparse(input_link)
    
    if parsed_url.netloc == 'www.youtube.com' and parsed_url.path == '/watch':
        return input_link
    elif parsed_url.netloc == 'youtu.be':
        video_id = parsed_url.path[1:]
        return f'https://www.youtube.com/watch?v={video_id}'
    else:
        return input_link

def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
def save_audio_to_file(audio_data, file_path):
    # Normalize the audio data to the range [-32768, 32767] for 16-bit depth
    normalized_audio = (audio_data * 32767).astype(np.int16)

    # Use scipy.io.wavfile.write to save the audio file
    write(file_path, 44100, normalized_audio)
        
def start_stop_recording(recording_status):
    if recording_status == 'start':
        # Start recording
        sd.default.samplerate = 44100  # Adjust the samplerate as needed
        sd.default.channels = 1  # Adjust the number of channels as needed

        global recording_buffer
        recording_buffer = []

        def callback(indata, frames, time, status):
            if status:
                print(status, flush=True)
            recording_buffer.append(indata.copy())

        with sd.InputStream(callback=callback):
            print("Recording... Press 'stop' to stop recording.", flush=True)
            sd.sleep(5000)  # Adjust the recording duration as needed
    elif recording_status == 'stop':
        # Stop recording and save to a WAV file
        print("Recording stopped.", flush=True)
        if recording_buffer:
            audio_data = np.concatenate(recording_buffer, axis=0)
            save_audio_to_file(audio_data, 'recorded_audio.wav')
            
def start_stop_recording_2(recording_status):
    if recording_status == 'start':
        # Start recording
        sd.default.samplerate = 44100  # Adjust the samplerate as needed
        sd.default.channels = 1  # Adjust the number of channels as needed

        global recording_buffer
        recording_buffer = []

        def callback(indata, frames, time, status):
            if status:
                print(status, flush=True)
            recording_buffer.append(indata.copy())

        with sd.InputStream(callback=callback):
            print("Recording... Press 'stop' to stop recording.", flush=True)
            sd.sleep(5000)  # Adjust the recording duration as needed
    elif recording_status == 'stop':
        # Stop recording and save to a WAV file
        print("Recording stopped.", flush=True)
        if recording_buffer:
            audio_data = np.concatenate(recording_buffer, axis=0)
            save_audio_to_file(audio_data, 'recorded_audio.wav')
            sound = pydub.AudioSegment.from_wav('recorded_audio.wav')
            sound.export('user_recorded_audio.mp3', format='mp3')
            
def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text
            

            
            
