from flask import Flask, render_template, request
from pipe import get_data
app = Flask(__name__, template_folder='frontend', static_folder='frontend')

saved_data = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = ''
    source_text = ''
    translated_text = ''
    summary = ''

    if request.method == 'POST':
        video_url = request.form['video_url']
        print(video_url)

        # Вызываем функцию get_data
        source_text, translated_text, summary = get_data(video_url)

        # Сохраняем данные в словаре
        saved_data[video_url] = {
            'source': source_text,
            'translated': translated_text,
            'summary': summary
        }

    return render_template('index.html', video_url=video_url, source_text=source_text, translated_text=translated_text, summary=summary)
if __name__ == '__main__':
    app.run(debug=True)