import openai
import json
import os
import string
import regex
import time
from collections import Counter

openai.api_key = 'this is your openai key'

def excute(data_path,start_idx):
    data = open(data_path, 'r')
    for k, example in enumerate(data):
        if k < start_idx:
            continue
        time.sleep(0.5)
        print(k)
        example = json.loads(example)
        q = example['question']
        answer = example['answer']
        try:
            rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content":
                    """Construct a global reasoning chain for this complex question [Question]:"{}" and answer the question, and generate a query to the
                    search engine based on what you already know at each step of the reasoning chain, starting with [Query].
                    You should generate the answer for each [Query], starting with [Answer].
                    You should generate the final answer for the [Question] by referring the [Query]-[Answer] pairs, starting with [Final Content].
                    For exmaple:
                    [Question]:"How many places of higher learning are in the city where the Yongle emperor greeted the person to whom the edict
                    was addressed?"
                    [Query 1]: Who was the edict addressed to?
                    [Answer 1]: the Karmapa
                    [Query 2]: Where did the Yongle Emperor greet the Karmapa?
                    [Answer 2]: Nanjing
                    [Query 3]: How many places of higher learning are in Nanjing?
                    [Answer 3]: 75
                    [Final Content]: The edict was addressed to Karmapa [1]. Yongle Emperor greet the Karampa in Nanjing [2]. There are 75 places
                    of higher learning are in Nanjing [3]. So the final answer is 75.
                    
                    [Question]:"Which magazine was started first Arthur’s Magazine or First for Women?"
                    [Query 1]: When was Arthur’s Magazine started?
                    [Answer 1]: 1844.
                    [Query 2]: When was First for Women started?
                    [Answer 2]: 1989
                    [Final Content]: Arthur’s Magazine started in 1844 [1]. First for Women started in 1989 [2]. So Arthur’s Magazine was started
                    first. So the final answer is Arthur’s Magazi
                    [Question]: {}
                    """.format(q, q)}
            ]
            )
        except:
            print('start_idx is {}'.format(k))
            return k
        predict_answer = rsp.get("choices")[0]["message"]["content"]
        print(predict_answer)
    return -1

if __name__ == '__main__':
    start_idx = 0
    while not start_idx == -1:
        start_idx = excute('/hotpotqa/hotpot_dev_fullwiki_v1_line.json',
               start_idx=start_idx)
        print('saved message')