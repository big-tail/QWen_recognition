import json
import streamlit as st
import requests
import base64

st.set_page_config(
    page_title="ChatApp",
    page_icon=" ",
    layout="wide",
)
st.title('欢迎使用通义千问大模型')

# 给对话增加history属性，将历史对话信息储存下来
if "history" not in st.session_state:
    st.session_state.history = []

# 显示历史信息
for message in st.session_state.history:
    if message:
        with st.chat_message(message['role']):
            st.text(message['content'][0]['text'])
            try:
                st.image(message['content'][1]['image'])
            except:
                continue

# TODO 修改text和fig为 *arg
def generate_session(role='user', text='', fig=''):
    session = {
        'role': role,
        'content': [
            {'text': text},
            {'image': fig}
        ]
    }
    return session


def get_response_material(history):
    model_url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'

    headers = {'Content-Type': 'application/json',
               'Authorization': 'sk-ac227686a13348d9a5fcf3857c36de48'}
    payload = {
        'model': 'qwen-vl-plus',
        'input': {
            'messages': history
        }
    }
    response_data = requests.request('POST', model_url, json=payload, headers=headers)
    return response_data.status_code, json.loads(response_data.text)


with st.sidebar:
    option = st.selectbox(
        '请选择图片上传方式',
        ['本地图片上传', '在线图片URL']
    )
    if option == '本地图片上传':
        if upload_files := st.file_uploader('请选择本地图片',
                                            type=['png', 'jpg', 'jpeg', 'tiff', 'bmp'],
                                            key='localImage'):
            image = upload_files.read()
            # st.write(image)df
            st.image(image)
    elif option == '在线图片URL':
        if image := st.text_input('请输入URL'):
            image
            st.image(image)
    else:
        # TODO 修改
        image = ''

# user_input接收用户的输入
if user_input := st.chat_input("Chat with 通义千问: "):
    # 在页面上显示用户的输入
    with st.chat_message("user"):
        st.markdown(user_input)

    # 将用户的输入加入历史
    st.session_state.history.append(generate_session('user', user_input, image))

    # get_response_material用来获取模型生成的回复，这个是需要根据自己的情况去实现
    # response为大模型生成的回复，material为RAG的检索的内容
    status_code, response = get_response_material(st.session_state.history)
    response
    # TODO 问答需要交替，修改报错后的数组添加逻辑
    if status_code == 200:
        response_content = response['output']['choices'][0]['message']['content']
        # 在页面上显示模型生成的回复
        with st.chat_message("assistant"):
            st.markdown(response_content)

        # 将模型的输出加入到历史信息中
        # TODO 需要修改
        st.session_state.history.append(generate_session('assistant', response_content))
        st.session_state.history
        # 只保留十轮对话，这个可根据自己的情况设定，我这里主要是会把history给大模型，context有限，轮数不能太多
        if len(st.session_state.history) > 20:
            st.session_state.messages = st.session_state.messages[-20:]

    else:
        st.session_state.history.pop()
        st.session_state.history
