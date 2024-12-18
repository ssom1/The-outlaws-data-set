import pandas as pd

# 엑셀 파일 읽기
file_path = '범죄도시_라벨_작성.xlsx'  # 본인의 파일 경로에 맞게 수정
df = pd.read_excel(file_path)

# 열 이름에 불필요한 공백 제거
df.columns = df.columns.str.strip()

# 'label'이 1 또는 0인 데이터만 필터링
df_filtered = df[df['label'].isin([1, 0])]

# 샘플링할 개수 지정
sampled_df = pd.DataFrame()

# 각 범죄도시별로 샘플링 전 데이터 개수 확인 및 샘플링
for label, sample_size in [('범죄도시1', 400), ('범죄도시2', 300), ('범죄도시3', 100), ('범죄도시4', 200)]:
    # 해당 범죄도시의 데이터 필터링
    available_data = df_filtered[df_filtered['series'] == label]
    available_count = len(available_data)
    print(f"{label} 데이터 개수: {available_count}")

    # 데이터가 충분할 경우 샘플링 진행
    if available_count >= sample_size:
        sampled_df = pd.concat([sampled_df, available_data.sample(n=sample_size, random_state=42)])
    else:
        print(f"{label}에서 충분한 데이터를 찾을 수 없습니다. 가능한 데이터 수: {available_count}")

# 결과 출력
print(sampled_df)

# 결과를 새로운 엑셀 파일로 저장 (샘플링된 데이터만 저장)
output_file_path = r'C:\temp\랜덤_샘플링_결과.xlsx'  # 저장할 경로
sampled_df.to_excel(output_file_path, index=False)

print(f"샘플링된 데이터를 {output_file_path}에 저장했습니다.")
