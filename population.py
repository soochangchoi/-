import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rc('font', family='Malgun Gothic')

# 파일 경로 리스트
file_paths = [
    "../광진구 공모전/2023년11월.xlsx - Sheet1.csv ",
    "../광진구 공모전/2023년12월.xlsx - Sheet1.csv",
    "../광진구 공모전/2024년11월.xlsx - Sheet1.csv",
    "../광진구 공모전/2024년12월.xlsx - Sheet1.csv",
    "../광진구 공모전/2024년1월.xlsx - Sheet1.csv",
    "../광진구 공모전/2024년2월.xlsx - Sheet1.csv",
    "../광진구 공모전/2025년 1월.xlsx - Sheet1.csv"
]

# 데이터프레임 불러오기 및 통합
dfs = []
for path in file_paths:
    df = pd.read_csv(path, encoding='utf-8')
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

# 승차/하차 컬럼 분리
boarding_columns = [col for col in combined_df.columns if '승차총승객수' in col]
alighting_columns = [col for col in combined_df.columns if '하차총승객수' in col]

# melt를 통해 데이터 재구성 (시간대 컬럼을 행으로)
melted_df = combined_df.melt(
    id_vars=['processed_station_name'],
    value_vars=boarding_columns + alighting_columns,
    var_name='시간대',
    value_name='승객수'
)

# 시간대 문자열 정리 (예: '00시승차총승객수' -> '00시 승차')
melted_df['시간대'] = melted_df['시간대'].str.replace('총승객수', '').str.replace('시', '시 ').str.strip()

# 시간 정렬용 숫자 추출
melted_df['정렬'] = melted_df['시간대'].apply(lambda x: int(x.split('시')[0]))

# 정류장별, 시간대별 승객수 집계
station_time_population = melted_df.groupby(
    ['processed_station_name', '시간대', '정렬']
)['승객수'].sum().reset_index()

# 시간대 정렬 후 불필요한 컬럼 제거
station_time_populations = station_time_population.sort_values(
    by=['processed_station_name', '정렬']
).drop(columns='정렬')
# '시간대' 컬럼에서 시각 숫자만 추출
station_time_populations['시각'] = station_time_populations['시간대'].str.extract(r'(\d+)').astype(int)

# 6시부터 10시 사이만 필터링
station_time_populations_filtered = station_time_populations[
    (station_time_populations['시각'] >= 6) & (station_time_populations['시각'] <= 10)
].drop(columns='시각')

# 결과 출력
print(station_time_populations_filtered)

# CSV 파일로 저장
station_time_populations_filtered.to_csv("station_time_populations_6시_10시.csv", index=False, encoding='utf-8-sig')

print(station_time_populations )

# CSV 파일로 저장
station_time_populations.to_csv("station_time_6_10.csv", index=False, encoding='utf-8-sig')
