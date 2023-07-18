from transformers import AutoTokenizer, AutoModel, BertJapaneseTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine
from database import Db

# 東北大学が開発した日本語BERTモデルとトークナイザーのロード
tokenizer = AutoTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
model = AutoModel.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')

# 東北大学のBERTモデルとトークナイザーのロード
# tokenizer = BertJapaneseTokenizer.from_pretrained('bert-base-japanese-v3')
# model = BertModel.from_pretrained('bert-base-japanese-v3')

# GPUが利用可能であればGPUを、そうでなければCPUを使用
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# モデルをデバイスに移動
model = model.to(device)

def compute_similarity(sentence1, sentence2):
    # 文章をトークン化し、モデルに入力できる形式に変換
    inputs1 = tokenizer(sentence1, return_tensors='pt', truncation=True, max_length=512, padding='max_length').to(device)
    inputs2 = tokenizer(sentence2, return_tensors='pt', truncation=True, max_length=512, padding='max_length').to(device)

    # モデルを使って文章の表現を計算
    with torch.no_grad():
        outputs1 = model(**inputs1)
        outputs2 = model(**inputs2)

    # 最初のトークン（[CLS]トークン）の表現を取得
    sentence_embedding1 = outputs1.last_hidden_state[0, 0]
    sentence_embedding2 = outputs2.last_hidden_state[0, 0]

    # コサイン類似度を計算
    similarity = 1 - cosine(sentence_embedding1.cpu(), sentence_embedding2.cpu())

    return similarity


def main():
    
    dbname = './gpt-suggest/db/tuboroxn.db'
    data = get_data(dbname)
    # 使用例
    text = data[2][-1]
    
    only_title = [d[-2] for d in data]
    only_content = [d[-1] for d in data]
    
    for title, content enumerate()
    

if __name__ == "__main__":
    # 2つの文章を定義
    sentence1 = "私は犬が好きです。"
    sentence2 = "それは機械学習を用いたメガネの学習です。"

    # 類似度を計算
    similarity = compute_similarity(sentence1, sentence2)
    print(f"Similarity: {similarity}")
