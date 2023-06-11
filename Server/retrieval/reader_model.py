from transformers import DPRReader, DPRReaderTokenizer
import pathlib, os
os.environ["CUDA_VISIBLE_DEVICES"] = '1'
device = "cuda"
tokenizer = DPRReaderTokenizer.from_pretrained("/dpr_reader_multi")
model = DPRReader.from_pretrained("/dpr_reader_multi")
model.eval()
model.to(device)

def get_answer(query,texts,title):
    encoded_inputs = tokenizer(
        questions=[query],
        titles=[title],
        texts=[texts],
        return_tensors="pt",
        max_length=510,
        )
    outputs = model(**encoded_inputs.to(device))
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    relevance_logits = outputs.relevance_logits


    answer_start_index = outputs.start_logits.argmax()
    answer_end_index = outputs.end_logits.argmax()
    predict_answer_tokens = encoded_inputs.input_ids[0, answer_start_index : answer_end_index + 1]
    #print(tokenizer.decode(predict_answer_tokens))
    answer = tokenizer.decode(predict_answer_tokens)
    return answer,relevance_logits
