from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
import pyperclip
import re
import os

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    video_url = request.form['video_url']
    video_id = extract_video_id(video_url)

    if video_id:
        try:
            transcript = get_transcript(video_id)
            return render_template('transcribe.html', video_url=video_url, transcript=transcript)
        except Exception as e:
            return render_template('error.html', error_message=str(e))
    else:
        return render_template('error.html', error_message='Invalid YouTube URL')

def extract_video_id(video_url):

    pattern = re.compile(r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})')
    match = pattern.match(video_url)
    if match:
        return match.group(1)
    else:
        return None





def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

  
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    file_path = os.path.join(downloads_folder, f"transcript_{video_id}.txt")

    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in transcript:
            file.write(f"{entry['text']}\n")

 
    clipboard_text = "\n".join([f"{entry['text']}" for entry in transcript])
    pyperclip.copy(clipboard_text)

    return transcript




if __name__ == '__main__':
    app.run(debug=True)
