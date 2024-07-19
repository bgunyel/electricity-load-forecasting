import time
import requests
import streamlit as st
from source.config import settings


def send_value_to_backend_server(value: int):
    backend_url = f'http://{settings.HOST}:{settings.BACKEND_PORT}/items/'
    response = requests.get(url=backend_url, params={'item_id': value})
    return response.json()


def print_value(value: int):
    print(f'Value: {value}')


def build_ui():
    st.title(settings.APPLICATION_NAME)

    st.write('Electricity')
    st.write('Load')
    st.write('is Forecasted')
    st.write('Here. :sunglasses:')

    number = st.select_slider(
        "Select a number",
        options=range(1, 10)
    )
    send_value = st.button(label='Send to Server')

    if send_value:
        response = send_value_to_backend_server(number)
        st.write("Response: ", response)


if __name__ == '__main__':
    build_ui()
