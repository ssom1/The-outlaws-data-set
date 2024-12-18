import MeCab
import pandas as pd
from gensim import corpora
from gensim.models import LdaModel

# 불용어 리스트
stop_word_list = ['영화', '영상', '배우', '장면']

# 명사 추출 함수
def extract_noun(text):
    t = MeCab.Tagger()
    parsed = t.parse(text)
    nouns = []
    for line in parsed.split('\n'):
        if line == 'EOS' or line == '':
            break
        try:
            word, features = line.split('\t')
            pos = features.split(',')[0]
            if pos == 'NNG' or pos == 'NNP':  # 일반명사(NNG), 고유명사(NNP)만 추출
                if len(word) >= 2:  # 2글자 이상
                    if word not in stop_word_list:  # 불용어 제외
                        nouns.append(word)
        except ValueError:
            continue  # 잘못된 라인은 무시
    return nouns

# 데이터 로드
data_path = "범죄도시1_라벨_작성.xlsx"
try:
    dataset = pd.read_excel(data_path).dropna(axis=0)  # 엑셀 파일 읽기
except Exception as e:
    print(f"파일 읽기 중 오류 발생: {e}")
    raise

# 데이터 확인
print("데이터셋 컬럼:", dataset.columns)

# 긍정(label=1)과 부정(label=0) 리뷰 추출
pos_text = list(dataset[dataset['label'] == 1]['Review'].values)
neg_text = list(dataset[dataset['label'] == 0]['Review'].values)

print("부정 리뷰 샘플:", neg_text[:3])

# 명사 추출
processed_texts = [extract_noun(doc) for doc in neg_text]
print("처리된 텍스트 샘플:", processed_texts[:3])

# Gensim 사전 및 코퍼스 생성
dictionary = corpora.Dictionary(processed_texts)
print("전체 명사의 수:", len(dictionary))

# 사전 필터링
dictionary.filter_extremes(no_below=5, no_above=0.5)
print("필터링 후 명사의 수:", len(dictionary))

# BOW (Bag-of-Words) 생성
corpus = [dictionary.doc2bow(text) for text in processed_texts]
print("BOW Corpus (샘플):", corpus[:3])

# LDA 모델링
num_topics = 5
lda_model = LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=num_topics,
    random_state=2024
)

# LDA 토픽 출력
for idx, topic in lda_model.print_topics(num_words=5):
    print(f"토픽 #{idx + 1}: {topic}")
