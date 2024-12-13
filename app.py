from flask import Flask, render_template, request
from summarizer import generate_summary

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        if request.method == 'POST':
            text = request.form['text'].strip()
            if len(text.split()) > 1000:
                return render_template('error.html', message="Text exceeds the 1000-word limit. Please try again.")
            if not text:
                return render_template('error.html', message="No text provided. Please enter some text to summarize.")
            
            summary = generate_summary(text, num_sentences=3)  # Adjust num_sentences as needed
            return render_template('result.html', text=text, summary=summary)
    except Exception as e:
        return render_template('error.html', message=f"An error occurred: {str(e)}")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="Page not found."), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', message="Internal server error. Please try again later."), 500


if __name__ == '__main__':
    app.run(debug=True)
