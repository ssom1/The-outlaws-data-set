import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
import MeCab

# 데이터 경로
data_path = "범죄도시4_라벨_작성.xlsx"

# 파일 읽기: 엑셀 파일로 처리
try:
    dataset = pd.read_excel(data_path).dropna(axis=0)  # 엑셀 파일 읽기
except Exception as e:
    print(f"파일 읽기 중 오류 발생: {e}")
    raise

# 컬럼 이름 확인
print("데이터셋 컬럼:", dataset.columns)

# 긍정(label=1)과 부정(label=0) 리뷰 텍스트 추출
try:
    pos_text = list(dataset[dataset['label'] == 1]['Review'].values)  # Review 컬럼 확인
    neg_text = list(dataset[dataset['label'] == 0]['Review'].values)
except KeyError as e:
    print(f"키 오류 발생: {e}. 컬럼 이름을 확인하세요.")
    raise

print("Positive texts (label=1):", pos_text[:3])
print("Negative texts (label=0):", neg_text[:3])

# 불용어 리스트
stop_word_list = ['범죄도시', '영상', '배우']

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

# 부정 텍스트에 대해 명사 추출
processed_texts = [extract_noun(doc) for doc in neg_text]
print("Processed texts (sample):", processed_texts[:3])

# Gensim 사전 및 코퍼스 생성
dictionary = corpora.Dictionary(processed_texts)
print("전체 명사의 수:", len(dictionary))

# 사전 필터링 (최소 5번 이상 등장하고, 전체 문서의 50% 이하에서 등장한 단어만 사용)
dictionary.filter_extremes(no_below=5, no_above=0.5)
print("필터링 후 명사의 수:", len(dictionary))

# BOW (Bag-of-Words) 생성
corpus = [dictionary.doc2bow(text) for text in processed_texts]
print("BOW Corpus (sample):", corpus[:3])

# LDA 모델링
num_topics = 5  # 토픽 수 설정
lda_model = LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=num_topics,
    random_state=2024
)

# 토픽 출력
print("\nLDA 토픽 결과:")
for idx, topic in lda_model.print_topics(num_words=5):
    print(f"토픽 #{idx + 1}: {topic}")
