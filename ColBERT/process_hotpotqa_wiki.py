import json
import bz2
import os
import csv
path = '/hotpotqa/enwiki-20171001-pages-meta-current-withlinks-abstracts'

def load_data(path=None):
    assert path
    corpus = []
    count = 0
    with open(
        '/hotpotqa/enwiki-20171001-pages-meta-current-withlinks-abstracts.tsv',
        'w', encoding='utf-8-sig') as w:
        writer = csv.writer(w, delimiter="\t")
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = root + '/' + file
                with bz2.open(file_path, 'r') as fin:
                    for line in fin.readlines():
                        data = json.loads(line)
                        row_text = ''
                        for text in data['text']:
                            row_text = row_text + ' ' + text
                        writer.writerow([count, 'Title: '+data['title']+' Text: '+row_text]) #pid \t passage text
                        count += 1
                        print(count)
    return corpus


load_data(path)
