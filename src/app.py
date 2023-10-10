import streamlit as st

import datetime


from calendar_api import get_events
from calendar_api import data_to_df

st.title('コストの可視化')

st.markdown("### 工数計算の期間を入力")
start_day = st.date_input("開始日", datetime.date(2023, 9, 1))
end_day = st.date_input("終了日", datetime.date(2023, 9, 30))


st.markdown("### 工数計算")


if st.button('実行'):
    calendar_data = get_events(start_day, end_day)
    calendar_df = data_to_df(calendar_data)
    st.write('以下が工数です．')
    st.dataframe(calendar_df) 


