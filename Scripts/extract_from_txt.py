from flask import Flask, request
from flask_cors import CORS
import json
import re

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
 
from transformers import pipeline
from keybert import KeyBERT 
 
@app.route('/', methods=['POST'])
def index():
    # body = json.loads(request.data)

    # Get body request
    body = request.get_json(force=True)

    # Get params request
    model = request.args.get('model')

    print(model)
    summarizer = pipeline("summarization", model=model)
    summary = summarizer(body, max_length = 250, min_length = 30)

    # clean text
    summary = summary[0]['summary_text'].replace(u'\xa0', u' ')

    # remove spaces
    summary = re.sub("\s\s+"," ",summary)

    # Get keyword
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(body)
    response = {
        "summary":summary,
        "keywords":keywords
    }
    return json.dumps(response)


if __name__ == '__main__':
    app.run(port=5000,debug=True)
