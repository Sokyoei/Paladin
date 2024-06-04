import streamlit as st


def set_header(header_name: str):
    st.header(header_name)
    st.sidebar.header(header_name)


def set_subheader(subheader_name: str):
    st.subheader(subheader_name)
    st.sidebar.subheader(subheader_name)
