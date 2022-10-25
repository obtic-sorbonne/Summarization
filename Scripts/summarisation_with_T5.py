if __name__ == "__main__":
    import argparse
    import os
    from bs4 import BeautifulSoup
    import pandas as pd
    from transformers import T5Tokenizer, FlaxT5ForConditionalGeneration

    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                      required=True,
                      help='path to the directory with XML-files'
                      )

    args = parser.parse_args()
    path = args.path

    def generate_dataframe(path_xml):
        data = {'filename': [], 'title': [], 'abstract': [], 'introduction': [], 'methods': [], 'results': [],
                'conclusion': []}
        for filename in os.listdir(path_xml):
            if filename.endswith('.xml'):
                with open(filename, 'r') as f:
                    soup = BeautifulSoup(f, 'lxml')
                    print('Working on ' + filename)
                    data['filename'].append(filename)
                    data['title'].append(soup.find('article-title').text.strip())
                    abstract, intro, method, res, concl = '', '', '', '', ''
                    for tag in soup.find_all('title'):
                        if tag.text.strip() == 'Abstract':
                            for p in tag.parent.find_all('p'):
                                abstract += p.text
                            data['abstract'].append(abstract)
                        elif 'Introduction' in tag.text.strip():
                            for p in tag.parent.find_all('p'):
                                intro += p.text
                            data['introduction'].append(intro)
                        elif 'method' in tag.text.lower().strip() and method == '':
                            for p in tag.parent.find_all('p'):
                                method += p.text
                            data['methods'].append(method)
                        elif 'result' in tag.text.lower().strip() and res == '':
                            for p in tag.parent.find_all('p'):
                                res += p.text
                            data['results'].append(res)
                        elif (
                                'conclusion' in tag.text.lower().strip() or 'discussion' in tag.text.lower().strip()) and concl == '':
                            for p in tag.parent.find_all('p'):
                                concl += p.text
                            data['conclusion'].append(concl)
                    if len(data['filename']) > len(data['methods']):
                        data['methods'].append('')
                    if len(data['filename']) > len(data['results']):
                        data['results'].append('')

        return pd.DataFrame.from_dict(data)
        #df.to_csv(r'data.csv', index=False, header=True)

    def summarize(df, j, section):
        text = list(df[section].values())[j]
        if type(text) != str:
            return ''
        else:
            cleaned_text = ""
            for i in range(len(text)):
                if text[i] != '"' or text[i] != "'" or text[i] != "‘" or text[i] != "’":
                    cleaned_text += text[i]
            ARTICLE_TO_SUMMARIZE = "summarize: " + cleaned_text
            inputs = tokenizer([ARTICLE_TO_SUMMARIZE], return_tensors="np")

            # Generate Summary
            summary_ids = model.generate(inputs["input_ids"]).sequences
            return tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)

    df = generate_dataframe(path)
    tokenizer = T5Tokenizer.from_pretrained("Samuel-Fipps/t5-efficient-large-nl36_fine_tune_sum_V2")
    model = FlaxT5ForConditionalGeneration.from_pretrained("Samuel-Fipps/t5-efficient-large-nl36_fine_tune_sum_V2",
                                                           from_pt=True)

    list_dict = ['abstract', 'introduction', 'methods', 'results', 'conclusion']
    result = {'filename': [], 'title': [], 'abstract': [], 'introduction': [], 'methods': [], 'results': [],
              'conclusion': []}
    for j, v in enumerate(df['filename'].values()):
        result['filename'].append(v)
        result['title'].append(list(df['title'].values())[j])
        for section in list_dict:
            print("Working on ", v, section)
            result[section] = summarize(df, j, section)

    df_sum = pd.DataFrame.from_dict(result)
    df_sum.to_csv(r'data_summaries.csv', index=False, header=True)
    #df_sum.to_excel(r'data_summaries.xlsx', index=False, header=True)
