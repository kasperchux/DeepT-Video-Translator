from flask import Flask, render_template, request, url_for, send_from_directory
from pipe import get_data
import os
app = Flask(__name__, template_folder='frontend', static_folder='frontend')

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = '' # Create pvariables
    source_text = ''
    translated_text = ''
    summary = ''
    video_path = os.path.abspath('frontend/my_video.mp4')

    if request.method == 'POST':
        video_url = request.form['video_url']

        # Call get_data, to get models predictions
        source_text, translated_text, summary = get_data(video_url)
        # video_path = url_for('frontend', filename='prepared.mp4')

    return render_template('index.html', video_url=video_url, source_text=source_text,
                               translated_text=translated_text, summary=summary, video_path=video_path)
if __name__ == '__main__': # Launch flask app
    app.run(debug=True)