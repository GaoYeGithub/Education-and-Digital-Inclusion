from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from gtts import gTTS

app = Flask(__name__)

os.makedirs('files', exist_ok=True)
os.makedirs('audio', exist_ok=True)

def get_audio_filename(text_filename):
    return f"{text_filename.split('.')[0]}.mp3"

@app.context_processor
def utility_processor():
    return {'get_audio_filename': get_audio_filename}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/CardAdd')
def CardAdd():
    return render_template('CardAdd.html')

@app.route('/Audio', methods=['GET', 'POST'])
def Audio():
    if request.method == 'POST':
        filename = request.form['filename']
        text = request.form['textbox']
        file_path = os.path.join('files', filename)
        audio_filename = get_audio_filename(filename)
        audio_path = os.path.join('audio', audio_filename)
        audio_name_path = os.path.join('audio', get_audio_filename('name_' + filename))

        with open(file_path, 'w') as file:
            file.write(text)
        tts = gTTS(text)
        tts.save(audio_path)
        tts_name = gTTS(filename)
        tts_name.save(audio_name_path)
        return redirect(url_for('Audio'))

    files = os.listdir('files')
    files_with_content_and_audio = [
        {
            'name': file,
            'content': open(os.path.join('files', file)).read() if os.path.isfile(os.path.join('files', file)) else "",
            'audio_exists': os.path.exists(os.path.join('audio', get_audio_filename(file))),
            'audio_name_exists': os.path.exists(os.path.join('audio', get_audio_filename('name_' + file)))
        }
        for file in files
    ]

    return render_template('Audio.html', files=files_with_content_and_audio)

@app.route('/audio/<filename>')
def get_audio(filename):
    return send_from_directory('audio', filename)

if __name__ == '__main__':
    app.run(debug=True)
