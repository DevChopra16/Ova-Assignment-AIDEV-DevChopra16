from flask import Flask, render_template, request, session, send_file
from llm_api import text_generator, caption_generator, image_generator, video_summary_generator, audio_to_text, text_to_audio, generate_summary
from utils import convert_to_markdown, process_uploaded_image, convert_to_base64, convert_to_video_address_link, extract_transcript_details, start_stop_recording, start_stop_recording_2, extract_text_from_pdf
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = 'dev162002'


@app.route('/')
def home():
    return render_template('home.html')

chat_history = []
@app.route('/text_conversion', methods=['GET', 'POST'])
def generate_result():
    global chat_history
    temp_history =[]
    if request.method == 'POST':
        chat_history.clear()
        user_input = request.form.get('user_input', '')

        if 'record' in request.form:
            start_stop_recording(request.form['record'])
            user_input = audio_to_text("recorded_audio.wav")

        # Add user input to chat history
        temp_history.append({'role': 'user', 'message': user_input})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input},
            ]
        )

        generated_text = response.choices[0].message.content

        # Add AI response to chat history
        temp_history.append({'role': 'ai', 'message': generated_text})
        
        chat_history = temp_history

    return render_template('text_conversion.html', chat_history=chat_history)

@app.route('/image_caption', methods=['GET', 'POST'])
def image_caption():
    if request.method == 'POST':
        uploaded_image = request.files['image']
        prompt = request.form.get('prompt', '')
        pil_image = process_uploaded_image(uploaded_image)
        encoded_image = convert_to_base64(pil_image)
        real_prompt = "You are an image caption generator. Generate a single line poetic and beautiful caption for the provided image, capturing the essence, emotion, or unseen magic within the visual tapestry."
        try:
            response = convert_to_markdown(caption_generator(user_prompt=real_prompt, image=pil_image))
        except Exception as e:
            response = "Gemini-Pro-Vision not responding"

        return render_template('image_caption.html', uploaded_image=encoded_image, prompt=prompt, image_caption=response)
    else:
        return render_template('image_caption.html')
    
@app.route('/generate_image', methods=['GET', 'POST'])
def generate_image_route():
    if request.method == 'POST':
        prompt = request.form.get('prompt', '')
        try:
            generated_image_url = image_generator(prompt)
        except Exception as e:
            generated_image_url = e
        return render_template('generate_image.html', prompt=prompt, generated_image_url=generated_image_url)
    else:
        return render_template('generate_image.html')
    
@app.route('/summarize_video', methods=['GET', 'POST'])
def summarize_video():
    youtube_link = None
    summary = None
    # image_filename = 'your_image.jpg'  # Replace with your actual filename
    external_image_url = None
    if request.method == 'POST':
        # Get the YouTube video link from the form
        youtube_link = request.form.get('youtube_link', '')

        if youtube_link:
            try:
                generalised_link = convert_to_video_address_link(youtube_link)
                video_id = generalised_link.split("=")[1]
                external_image_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"
            except Exception as e:
                summary = "Enter a valid YouTube video link"
            
        try:
            
            transcript_text = extract_transcript_details(generalised_link)
            
            if transcript_text:
                
                try:
                    
                    summary = convert_to_markdown(video_summary_generator(transcript_text))
                    
                except Exception as err:
                    summary = "Gemini Pro API not responding. Try later."
                    
        except Exception as errr:
            summary = "Transcripts unavailable for the provided video."

    return render_template('summarize_video.html', youtube_link=youtube_link, summary=summary, external_image_url = external_image_url)

@app.route('/audio_conversation', methods=['GET', 'POST'])
def audio_conversation():
    if 'user_audio' not in session:
        session['user_audio'] = []

    if request.method == 'POST':
        recording_status = request.form.get('record', '')
        start_stop_recording_2(recording_status)

        # Add user's recorded audio to the session
        user_audio_path = 'user_recorded_audio.mp3'
        session['user_audio'].append(user_audio_path)

        user_input = audio_to_text("recorded_audio.wav")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input},
            ]
        )

        generated_text = response.choices[0].message.content

        # Generate AI response audio
        text_to_audio(generated_text)
        session['ai_audio'] = "ai_speech.mp3"

    return render_template('audio_conversation.html', user_audio=session['user_audio'], ai_audio=session.get('ai_audio'))

@app.route('/download_user_audio', methods=['GET'])
def download_user_audio():
    user_audio_path = session['user_audio'][-1] if session['user_audio'] else ''
    return send_file(user_audio_path, as_attachment=True)

@app.route('/download_ai_audio', methods=['GET'])
def download_ai_audio():
    ai_audio_path = session.get('ai_audio', '')
    return send_file(ai_audio_path, as_attachment=True)


@app.route('/pdf_summary', methods=['GET', 'POST'])
def pdf_summary():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            # Save the uploaded PDF file
            pdf_file_path = os.path.join('uploads/', pdf_file.filename)
            pdf_file.save(pdf_file_path)

            # Extract text from the PDF
            pdf_text = extract_text_from_pdf(pdf_file_path)

            # Generate summary using OpenAI GPT-3.5-turbo
            pdf_summary = convert_to_markdown(generate_summary(pdf_text))

            # Save the summary in the session for display
            session['pdf_summary'] = pdf_summary
            return render_template('pdf_summary.html', pdf_summary=pdf_summary)

    # Render the initial page
    return render_template('pdf_summary.html', pdf_summary=None)

if __name__ == '__main__':
    app.run(debug=True)
