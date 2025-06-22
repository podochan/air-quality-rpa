import streamlit as st 
import pandas as pd 
import requests 
from datetime import datetime



#OpenWeatherMap 미세먼지 데이터 수집 함수

def fetch_air_quality_data(lat=37.57, lon=126.98):  # 서울 좌표 
  API_KEY = 'd90ea6c0fa663b9855fe860eeb0bccc7'  
  url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}" 
  response = requests.get(url) 
  data = response.json()

  if 'list' in data and len(data['list'])>0:
   ts = datetime.now()
   pm10 = data['list'][0]['components']['pm10']
   df = pd.DataFrame({   'dataTime': [ts], 'pm10Value': [pm10]}) 
   return df

  else:
   return pd.DataFrame()



#활동 점수 계산 함수

def calculate_activity_score(df): 
    df['activityScore'] = 100 - df['pm10Value'] * 0.8 
    return df



#Streamlit 대시보드


st.set_page_config(page_title='실시간 미세먼지 대시보드', layout='wide') 
st.title('🌫️ 실시간 미세먼지 & 활동 추천 대시보드')

city_options = { '서울': (37.57, 126.98), '부산': (35.18, 129.07), '대구': (35.87, 128.60), '광주': (35.16, 126.85), '제주': (33.50, 126.53) }

city = st.selectbox('도시를 선택하세요:', list(city_options.keys())) 
lat, lon = city_options[city] 
df = fetch_air_quality_data(lat, lon)

if not df.empty: 
    df = calculate_activity_score(df)

    st.subheader(f"📍 {city} 현재 미세먼지 (PM10) 및 활동 점수")
    st.metric(label="PM10 농도 (㎍/㎥)", value=f"{df['pm10Value'][0]:.1f}")
    st.metric(label="활동 점수", value=f"{df['activityScore'][0]:.1f}")

    if df['pm10Value'][0] < 40 and df['activityScore'][0] > 70:
     st.success("👍 지금은 야외 활동하기 좋은 시간입니다!")
    else:
     st.warning("😷 실외 활동은 주의가 필요해요")

else:
    st.error('데이터를 불러오지 못했습니다. API 키를 확인하거나 잠시 후 다시 시도해주세요.')

