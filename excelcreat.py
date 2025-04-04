#@gemini_test.py를 분석해서 Gemini API 사용방법을 파악하고, 아래 기능을 하는 콘텐츠생성하기.py 파일을 만들고 실행해

#1. data.xlsx 파일을 읽어서 A열의 블로그 제목을 가져오기
#2. 각 제목마다 Gemini API로 서론/본론/결론 구조의 블로그 콘텐츠 생성하기
#3. 생성된 콘텐츠를 엑셀 B열에 저장하기
#4. 2행부터 마지막 행까지 자동으로 처리하고, 진행상황 출력하기
#5. 모든 처리가 끝나면 결과를 data.xlsx에 저장하기
import google.generativeai as genai
import pandas as pd
import time

# API 키 설정
GOOGLE_API_KEY = "AIzaSyBY_CPLpmp79tX5h7gR8G6b96Z8mmoyDPM"
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini 모델 설정
model = genai.GenerativeModel('gemini-2.0-flash')

# 엑셀 파일 읽기
df = pd.read_excel('data.xlsx')

# 2행부터 마지막 행까지 반복
for index in range(1, len(df)):
    title = df.iloc[index, 0]  # A열의 제목
    
    # 프롬프트 생성
    prompt = f"""
    다음 블로그 제목에 대한 상세한 블로그 포스트를 작성해주세요:
    제목: {title}
    
    다음 형식으로 작성해주세요:
    1. 서론
    2. 본론
    3. 결론
    
    각 섹션은 2-3문단으로 구성해주세요.
    """
    
    try:
        # Gemini API 호출
        response = model.generate_content(prompt)
        content = response.text
        
        # B열에 콘텐츠 저장
        df.iloc[index, 1] = content
        
        # 진행 상황 출력
        print(f"처리 완료: {index}/{len(df)} - {title}")
        
        # API 호출 간격 조절
        time.sleep(1)
        
    except Exception as e:
        print(f"오류 발생: {title} - {str(e)}")
        continue

# 결과 저장
df.to_excel('data.xlsx', index=False)
print("모든 처리가 완료되었습니다.")

