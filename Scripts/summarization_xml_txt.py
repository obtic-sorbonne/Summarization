from flask import Flask, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import re

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

from transformers import pipeline
from keybert import KeyBERT


@app.route('/', methods=['POST'])
def extract_from_xml(filename):
    data = {}
    soup = BeautifulSoup(filename, 'lxml')
    abstract, intro, method, result, concl = ('' for i in range(5))
    for tag in soup.find_all('title'):
        if tag.text.strip() == 'Abstract':
            for p in tag.parent.find_all('p'):
                abstract += p.text
            data['Abstract'] = abstract.strip()
        elif 'Introduction' in tag.text.strip():
            for p in tag.parent.find_all('p'):
                intro += p.text
            data['Introduction'] = intro.strip()
        elif 'method' in tag.text.lower().strip() and method == '':
            for p in tag.parent.find_all('p'):
                method += p.text
            data['Methods'] = method.strip()
        elif 'result' in tag.text.lower().strip() and result == '':
            for p in tag.parent.find_all('p'):
                result += p.text
            data['Results'] = result.strip()
        elif ('conclusion' in tag.text.lower().strip() or 'discussion' in tag.text.lower().strip()) and concl == '':
            for p in tag.parent.find_all('p'):
                concl += p.text
            data['Conclusion'] = concl.strip()

    return data

def index(url):
    if url:
        res = requests.get(url)
        data = extract_from_xml(res.text)
        model = request.args.get('model')
        response = []
        summarizer = pipeline("summarization", model=model)
        for k, v in data.items():
            if len(v) > 0:
                title = k
                summary = summarizer(v, max_length=250, min_length=30)

        # clean text
                summary_result = summary[0]['summary_text'].replace(u'\xa0', u' ')
                if model == 't5-large':
                    summary = '. '.join([x.strip().capitalize() for x in summary_result.split('.')])
                else:
                    summary = summary_result

        # Get keyword
                kw_model = KeyBERT()
                keywords = kw_model.extract_keywords(v)
                response_element = {"title": title,
                    "summary": summary.strip(),
                    "keywords": keywords
                }
            response.append(response_element)
    else:

        # body = json.loads(request.data)

        # Get body request
        body = request.get_json(force=True)

        # Get params request
        model = request.args.get('model')

        print(model)
        summarizer = pipeline("summarization", model=model)
        summary = summarizer(body, max_length=250, min_length=30)

        # clean text
        summary = summary[0]['summary_text'].replace(u'\xa0', u' ')

        # remove spaces
        summary = re.sub("\s\s+", " ", summary)

        # Get keyword
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(body)
        response = {
            "summary": summary,
            "keywords": keywords
        }
    return json.dumps(response)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
