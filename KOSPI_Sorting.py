import pandas as pd
import datetime

df = pd.read_excel("KOSPI200_202404280419.xlsx")

df = df.replace(r'^\s*$',"NaN", regex=True)
df = df.fillna(0)

# 특정 열을 제외한 모든 열의 데이터를 float 또는 int로 변환
columns_to_exclude = ['Company']  # 변환하지 않을 열을 지정

for column in df.columns:
    if column not in columns_to_exclude and df[column].dtype == 'object':
        try:
            df[column] = df[column].str.replace(',','').astype(float)  # 또는 int로 변환
        except ValueError:
            pass

# df['2021년 부채비율'] = df['2021년 부채비율'].astype(float)  # 또는 int로 변환
# df['2021년 부채비율'] = df['2021년 부채비율'].str.replace(',', '').astype(float)
# df['2022년 부채비율'] = df['2022년 부채비율'].str.replace(',', '').astype(float)
# df['2023년 부채비율'] = df['2023년 부채비율'].str.replace(',', '').astype(float)

condition1 = df['2022년 당기순이익'] > df['2021년 당기순이익']
condition2 = df['2023년 당기순이익'] > df['2022년 당기순이익']
condition3 = df['2024년 당기순이익'] > df['2023년 당기순이익']

# condition4 = df['2021년 당좌비율'] > 100
# condition5 = df['2022년 당좌비율'] > 100
condition6 = df['2023년 당좌비율'] > 100

# condition7 = df['2021년 부채비율'] < 100
# condition8 = df['2022년 부채비율'] < 100
condition9 = df['2023년 부채비율'] < 100

condition10 = df['미래PER'] < 15

# 조건을 만족하는 행만 선택
# filtered_df = df[
#                 condition1 & condition2 & condition3 &
#                 condition4 & condition5 & condition6 &
#                 condition7 & condition8 & condition9 &
#                 condition10
#                  ]

filtered_df = df[
                condition1 & condition2 & condition3 &
                condition6 &
                condition9 &
                condition10
                 ]


# 인덱스 조정
filtered_df.reset_index(drop=True, inplace=True)

# 새로운 엑셀 파일로 저장


date = datetime.datetime.now().strftime("%m%d_%H%M%S")

filtered_df.to_excel('test_'+ date +'.xlsx', index=False)

# 저장 확인 메시지
print("새로운 엑셀 파일이 저장되었습니다.")
