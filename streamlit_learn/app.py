import streamlit as st  # noqa: I001

from utils import set_header, set_subheader

st.set_page_config(page_title="streamlit learn", page_icon="🦊")


def base():
    set_header("基础")


def images():
    set_header("图像")

    set_subheader("图片")
    st.image("../../data/Ahri/Popstar Ahri.jpg")

    set_subheader("地图")
    data = {
        'latitude': [37.7749, 34.0522, 40.7128],
        'longitude': [-122.4194, -118.2437, -74.0060],
        'name': ['San Francisco', 'Los Angeles', 'New York'],
    }
    st.map(data, zoom=4, use_container_width=True)

    set_subheader("摄像头")
    img = st.camera_input("输入图片")
    if img:
        st.image(img)


def main():
    page_functions = {"基础": base, "图像": images}
    page = st.sidebar.selectbox("例子", page_functions.keys())
    page_functions[page]()


if __name__ == '__main__':
    main()
