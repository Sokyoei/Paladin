import streamlit as st

st.title("streamlit learn")

st.header("基础")

st.header("图像")

st.subheader("地图")
data = {
    'latitude': [37.7749, 34.0522, 40.7128],
    'longitude': [-122.4194, -118.2437, -74.0060],
    'name': ['San Francisco', 'Los Angeles', 'New York'],
}
st.map(data, zoom=4, use_container_width=True)

st.subheader("摄像头")
img = st.camera_input("输入图片")
if img:
    st.image(img)
