import streamlit as st
import requests
import json

# test_URL='http://52.53.254.178:8080/test'
URL = 'http://54.219.177.99/api'

def fetch_api(session,url,my_ip_json):
    # try:
    result = session.post(url, json = my_ip_json)
    # result = session.get(url)
    return result
    # except Exception:
    #     return {}


# def interact_api(session):
#     with st.form("my_form"):
        
#              # """ add endpoint below : """
#             data = fetch_api(session, f"https://picsum.photos/id/{index}/info")
#             if data:
#                 # """process op from api"""
#                 st.write(data)
#                 st.image(data['download_url'], caption=f"Author: {data['author']}")  #data['download_url']  = "download_url":"https://picsum.photos/id/0/5616/3744" for image with id = 0
#             else:
#                 st.error("Error")

def api_op(my_ip):
    my_ip_json = {"img_string" : my_ip}
    # x = requests.get(URL, data = my_ip_json)
    # x = requests.get(test_URL, params = my_ip_json)
    # st.write(x)
    session = requests.Session()
    data = fetch_api(session, URL, my_ip_json)
    # print(data.text)
    string_dict=data.text
    op_dict = json.loads(string_dict)
    mask_string_ = op_dict["mask_string"]
    return mask_string_
