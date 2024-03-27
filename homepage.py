import streamlit as st
import Chat_With_QWen
from http import HTTPStatus

ctyun_icon = open(r'figures\\CTyun_logo.png',mode='rb').read()
st.set_page_config(
    page_title="ChatApp",
    page_icon=ctyun_icon,
    layout="wide"
)
st.title('欢迎使用通义千问大模型')

### 可视化对话信息
def display_chat(message):
    role = message['role']
    content = message['content']
    with st.chat_message(role):
        for info in content:
            for key,value in info.items():
                st.markdown(value, unsafe_allow_html=True)


### 初始化对话信息
if "history" not in st.session_state:
    st.session_state["history"] = []
if 'image_upload_method' not in st.session_state:
    st.session_state["image_upload_method"] = "online"
if "input_pictures" not in st.session_state:
    st.session_state["input_pictures"] = []     
    
### 展示历史对话信息    
for message in st.session_state["history"]:
    display_chat(message)

### 侧边图片上传栏
with st.sidebar:
    
    import tkinter as tk
    from tkinter import filedialog

    option = st.radio(
        '请选择图片上传方式',
        ['本地图片', '网络图片'],
        index=1
    )
    ### 本地图片上传
    if option == "本地图片":
        # 设置tkinter
        root = tk.Tk()
        root.withdraw()
        # 让文件选择框置顶在屏幕中
        root.wm_attributes('-topmost', 1)
        # 点击按钮弹出选择框
        clicked = st.button('打开文件夹')
        if clicked:
            picture_names = filedialog.askopenfilenames(
                title='选择图片',
                filetypes=[('可选择的图片类型',
                            ['*.png', '*.jpg', '*.jpeg', '*.tiff', '*.bmp']
                            )],
                master=root
            )
            for picture_name in picture_names:
                st.session_state['image_upload_method'] = 'local'
                st.session_state["input_pictures"].append(''.join(['file://',picture_name]))
    ### 网络图片上传
    elif option == "网络图片":
        picture_url = st.text_input('请输入图片的URL')
        clicked = st.button("添加图片URL")
        if clicked and picture_url not in st.session_state["input_pictures"]:
            exist_code = Chat_With_QWen.check_online_image_exist(picture_url)
            if exist_code == HTTPStatus.OK:
                st.session_state['input_pictures'].append(picture_url)
            else:
                st.text('填入的图片不存在')
            


### 接收用户的输入
if user_input := st.chat_input("Chat with 通义千问: "):

    ### 格式化输入的信息
    format_messages = Chat_With_QWen.dispose_input_to_message('user',
                                               user_input=user_input,
                                               images=st.session_state["input_pictures"])

    st.session_state["input_pictures"] = []
    st.session_state['history'].append(format_messages)
    
    ### 在页面上显示用户的输入
    display_chat(format_messages)
    ### 如果历史对话中不包含本地图片，使用http请求
    if st.session_state['image_upload_method'] == 'online':
        response = Chat_With_QWen.conversation_call_with_http(st.session_state['history'])
        status_code,response_message= Chat_With_QWen.dispose_response_message(response)
        if status_code == HTTPStatus.OK:
            st.session_state['history'].append(response_message)
            # 展示大模型返回信息
            display_chat(response_message)
        else:
            st.session_state['history'].pop()
    ### 如果历史对话中包含本地图片，使用SDK请求      
    else:
        response = Chat_With_QWen.conversation_call_with_sdk(st.session_state['history'])
        status_code,response_message= Chat_With_QWen.dispose_response_message(response)
        ### 成功返回信息则展示，错误则弹出会话
        if status_code == HTTPStatus.OK:
            st.session_state['history'].append(response_message)
            ### 可视化返回信息
            display_chat(response_message)
        else:
            with st.chat_message('assistant'):
                st.error('服务器响应异常')
            st.session_state['history'].pop()
            
    ### 设置保存的最大历史会话数  
    if len(st.session_state.history) > 20:
        st.session_state.messages = st.session_state.messages[-20:]

