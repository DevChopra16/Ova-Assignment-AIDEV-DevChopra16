# Smart AI Flask App

This Flask web application leverages various OpenAI models to provide a versatile set of features for text, audio, image, and video processing. The project integrates different OpenAI APIs, including Whisper, tts-1, DALL-E-3, GPT 3.5 turbo, and Google's Gemini Pro Vision Model.

## Features

### Text Conversion

The Text Conversion module allows users to interact with the GPT 3.5 turbo model by entering text messages. Users can have dynamic conversations, receive detailed responses, and explore the capabilities of the powerful language model.

### Audio Conversation

The Audio Conversation feature enables users to engage in spoken conversations with the OpenAI Whisper 1 model. Users can record their voice, convert it to text, and receive responses in both written and spoken formats.

### Image Generation

The Image Generation module utilizes the DALL-E-3 model to generate unique images based on user prompts. Users can input creative prompts, and the model responds with visually intriguing images.

### Image Caption

The Image Caption feature integrates Google's Gemini Pro Vision Model to provide descriptive captions for uploaded images. Users can upload an image and receive natural language descriptions generated by the vision model.

### Summarize YouTube Video

This module leverages Google's Gemini Pro to summarize YouTube videos. Users can input a YouTube video link, and the model generates a concise summary along with an accompanying image related to the video content.

### Summarize PDF

The Summarize PDF feature enables users to upload PDF documents, and GPT 3.5 turbo generates a summary of the document's content. This provides a quick overview of lengthy documents.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/DevChopra16/Ova-Assignment-AIDEV-DevChopra16.git
2. Install dependencies
   ```bash
   pip install -r requirements.txt
3. Run the following command in terminal
   ```bash
   python app.py
4. Access the application in your web browser at http://localhost:5000
