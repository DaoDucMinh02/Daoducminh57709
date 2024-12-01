from flask import Flask, render_template, request
from summarizer import generate_summary

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        text = request.form['text']
        summary = generate_summary(text, num_sentences=3)  # Adjust num_sentences as needed
        return render_template('result.html', text=text, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
