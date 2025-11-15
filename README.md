## This is the project for Search-in-the-Chain
Welcome to read our paper：https://arxiv.org/abs/2304.14732
```
@inproceedings{xu2024search,
  title={Search-in-the-chain: Interactively enhancing large language models with search for knowledge-intensive tasks},
  author={Xu, Shicheng and Pang, Liang and Shen, Huawei and Cheng, Xueqi and Chua, Tat-Seng},
  booktitle={Proceedings of the ACM Web Conference 2024},
  pages={1362--1373},
  year={2024}
}
```
**You can start Searchain quickly from LLamaIndex: [here](https://github.com/run-llama/llama_index/tree/main/llama-index-packs/llama-index-packs-searchain)**

You can try to run our project by following the steps below, running in different environments may encounter various problems. We are still working hard to make it robust and bug-free. 
#### 1. Index your corpus via ColBERT
   Process your data into a format suitable for ColBERT indexing 
   ```
   python ColBERT/process_hotpotqa_wiki.py
   ```
   Indext your data
   ```
   python ColBERT/index.py
   ```
   Run the service for retrieval
   ```
   python ColBERT/server_retrieval.py
   ```
#### 2. Run the serive for verification and completion in Information Retrieval
```
python Server/server.py
```
#### 3. Construct Chain-of-Query and and interact with search service (communicate with Server/server.py)
An example on HotpotQA in the setting without IR:
```
python SearChain_without_IR.py
```
An example on HotpotQA in the setting with IR:
```
python SearChain_w_IR.py
```

