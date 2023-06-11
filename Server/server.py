from retrieval import reader_model
import pathlib, os
os.environ["CUDA_VISIBLE_DEVICES"] = '1'
device = "cuda"
import torch
import regex
import string
from sentence_transformers import CrossEncoder
import requests
model_cross_encoder = CrossEncoder('/Quora_cross_encoder',device=device)
model_cross_encoder.model.eval()

def normalize_answer(s):
    def remove_articles(text):
        return regex.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def match_or_not(prediction, ground_truth):
    norm_predict = normalize_answer(prediction)
    norm_answer = normalize_answer(ground_truth)
    return norm_answer in norm_predict


def have_seen_or_not(query_item,query_seen_list,query_type):
    if 'Unsolved' in query_type:
        return False
    for query_seen in query_seen_list:
        if model_cross_encoder.predict([(query_seen, query_item)]) > 0.5:
            return True
    return False

if __name__ == '__main__':
    import socket
    print('Loading data....')
    HOST = '10.208.62.21'
    PORT = 50007
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print('Waiting for connection...')
    sum_cite = 0
    good_cite = 0
    dic_question_answer_to_reference = []
    ques_idx = 0
    #start_idx = 0
    with torch.no_grad():
        while True:
            connection,address = sock.accept()
            print('connect success from {}'.format(address))
            continue_label = True
            query_seen_list = []
            start = True
            break_flag = False
            while continue_label:
                continue_label = False
                #try:
                #connection.settimeout(5)
                buf = connection.recv(10240)
                query = buf.decode()
                print('recv query is {}'.format(query))
                if query == 'end':
                    break_flag = True
                    break
                query_list = query.split('\n')
                message = ''
                for idx in range(len(query_list)):
                    query_item = query_list[idx]
                    if 'Query' in query_item and ']:' in query_item:
                        temp = query_item.split(']')
                        if len(temp) < 2:
                            continue
                        query_type = temp[0]
                        query_item = temp[1]
                        if ':' in query_item:
                            query_item = query_item[1:]
                        print('solving: '+query_item)
                        if not have_seen_or_not(query_item,query_seen_list,query_type):
                            now_reference = {}
                            query_seen_list.append(query_item)
                            # I, corpustext_list_topk, corpus_list_topk = retrieval_model_hotpotqa.retrieval_topk(corpus_dict=corpus_dict, corpus_id=corpus_ids,
                            #                                                            query=query_item, index=index, k=10)
                            url = 'http://localhost:8893/api/search?query='+query_item+'&k=1'
                            response = requests.get(url=url)
                            res_dic = response.json()
                            corpus_list_topk = res_dic['topk']
                            #print(corpus_list_topk)
                            top1_passage = corpus_list_topk[0]['text']
                            #top1_passage = retrieval_model_hotpotqa.rerank_topk_colbert(corpus_list_topk, query_item)
                            answer,relevance_score = reader_model.get_answer(query=query_item,texts='',title=top1_passage)
                            now_reference['query'] = query_item
                            now_reference['answer'] = answer
                            now_reference['reference'] = top1_passage
                            now_reference['ref_score'] = relevance_score
                            now_reference['idx'] = ques_idx
                            dic_question_answer_to_reference.append(now_reference)

                            print('answer is '+answer)
                            print('reference is'+top1_passage)
                            print('score is {}'.format(relevance_score))
                            sum_cite += 1
                            print('query_type is '+query_type)
                            if 'Unsolved' in query_type:
                                message = '[Unsolved Query]:{}<SEP>[Answer]:{}<SEP>[Reference]:{}<SEP>'.format(query_item,
                                                                                                               answer,
                                                                                                               top1_passage)
                                print(message)
                                continue_label = True
                                if relevance_score > 1.5:
                                    good_cite += 1
                                break
                            elif relevance_score > 1.5:
                                good_cite += 1
                                answer_start_idx = idx+1
                                predict_answer = ''
                                while answer_start_idx < len(query_list):
                                    if 'Answer' in query_list[answer_start_idx]:
                                        predict_answer = query_list[answer_start_idx]
                                        break
                                    answer_start_idx += 1
                                print('predict answer is '+predict_answer)
                                match_label = match_or_not(prediction=predict_answer,ground_truth=answer)
                                if match_label:
                                    continue
                                else:
                                    message = '[Query]:{}<SEP>[Answer]:{}<SEP>[Reference]:{}<SEP>'.format(query_item,
                                                                                             answer,
                                                                                             top1_passage)
                                    print(message)
                                    continue_label = True
                                    break
                if continue_label:
                    connection.send(message.encode())
                else:
                    connection.send('end'.encode())
            while True:
                data = connection.recv(1024)
                if not data:
                    break
            if not break_flag:
                ques_idx += 1

            connection.close()