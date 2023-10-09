import streamlit as st

import datetime

from calendar_api import service_google_calendar
from calendar_api import get_events

st.title('コストの可視化')

st.markdown("### 工数計算の期間を入力")
d = st.date_input("開始日", datetime.date(2023, 9, 1))
d = st.date_input("終了日", datetime.date(2023, 9, 30))


st.markdown("### 工数計算")

#st.button("工数計算")

if st.button('実行'):
    st.write('以下が工数です．')

