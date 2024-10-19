from flask import Flask, request, render_template
import PyPDF2
from transformers import pipeline

# Initialize the summarizer using T5 model
summarizer = pipeline("summarization", model='t5-base', tokenizer='t5-base', framework='pt')

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html', content=None, summary=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text() + '\n'

        # Generate summary
        summary = summarizer(text, max_length=200, min_length=100, do_sample=False)

        # Return the rendered template with both text and summary
        return render_template('upload.html', content=text, summary=summary[0]['summary_text'])
    return "Invalid file format"

if __name__ == '__main__':
    app.run(debug=True)
