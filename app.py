from flask import Flask, render_template, request
from pipe import get_data
app = Flask(__name__, template_folder='frontend', static_folder='frontend')

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = '' # Create variables
    source_text = ''
    translated_text = ''
    summary = ''

    if request.method == 'POST': 
        video_url = request.form['video_url']

        # Call get_data, to get models predictions
        source_text, translated_text, summary = get_data(video_url)
        
    return render_template('index.html', video_url=video_url, source_text=source_text,
                               translated_text=translated_text, summary=summary)
if __name__ == '__main__': # Launch flask app
    app.run(debug=True)