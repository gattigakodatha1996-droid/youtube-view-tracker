import streamlit as st
import pandas as pd
from supabase import create_client

# 1. Connect to your Supabase Vault
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

st.title("📊 Matrix Video Performance")

# 2. Fetch Video List
video_data = supabase.table("videos").select("*").execute()
videos = {v['title']: v['id'] for v in video_data.data}

# 3. Sidebar for Video Selection
selected_video_name = st.sidebar.selectbox("Choose a Video to Track:", list(videos.keys()))
video_id = videos[selected_video_name]

# 4. Fetch Snapshots (Views over time)
stats = supabase.table("snapshots").select("*").eq("video_id", video_id).order("checked_at").execute()
df = pd.DataFrame(stats.data)

if not df.empty:
    # 5. Calculate Daily Gain (Today - Yesterday)
    df['daily_gain'] = df['views'].diff()
    df['Date'] = pd.to_datetime(df['checked_at'])

    # 6. Show the Total Views Line Chart
    st.subheader(f"Total Views for {selected_video_name}")
    st.line_chart(df, x="Date", y="views")

    # 7. Show the Growth Bar Chart
    st.subheader("Daily Growth (New Views)")
    st.bar_chart(df, x="Date", y="daily_gain")
else:
    st.info("No data yet! The daily tracker runs at midnight.")
