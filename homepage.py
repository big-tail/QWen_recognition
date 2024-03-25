import streamlit as st

chat = None

st.set_page_config(
    page_title="ChatApp",
    page_icon=" ",
    layout="wide",
)
st.title('欢迎使用通义千问大模型')


def increase_rows():
    if len(st.session_state['input_pictures']) < 5:
        st.session_state['input_pictures'].append('')


if "history" not in st.session_state:
    st.session_state["history"] = []

with st.sidebar:
    import tkinter as tk
    from tkinter import filedialog

    sidebar_placeholder = st.empty()
    option = st.selectbox(
        '请选择图片上传方式',
        ['本地图片', '网络图片']
    )
    if "input_pictures" not in st.session_state:
        st.session_state["input_pictures"] = []
    if option == "本地图片":
        # with sidebar_placeholder.container():
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
                    st.write(picture_name)
                    st.image(picture_name)
                    st.session_state["input_pictures"].append(picture_name)

    elif option == "网络图片":
        picture_url = st.text_input('请输入图片的URL')
        clicked = st.button("添加图片URL")
        st.write(len(st.session_state["input_pictures"]))
        if clicked and len(st.session_state["input_pictures"]) < 5 \
                and picture_url not in st.session_state["input_pictures"]:
            st.session_state['input_pictures'].append(picture_url)
        st.write(st.session_state['input_pictures'])

    # if st.button("上传图片"):
    #     st.session_state["input_pictures"] = []
    # st.write(st.session_state['input_pictures'])


# user_input接收用户的输入
if user_input := st.chat_input("Chat with 通义千问: "):
    # 在页面上显示用户的输入
    with st.chat_message("user"):
        st.markdown(user_input)
    #重置sidebar中已输入的图片信息
    st.write(st.session_state["input_pictures"])
    st.session_state["input_pictures"] = []

    # # 将用户的输入加入历史
    # st.session_state.history.append(generate_session('user', user_input, image))
    #
    # # get_response_material用来获取模型生成的回复，这个是需要根据自己的情况去实现
    # # response为大模型生成的回复，material为RAG的检索的内容
    # status_code, response = get_response_material(st.session_state.history)
    # response
    # # TODO 问答需要交替，修改报错后的数组添加逻辑
    # if status_code == 200:
    #     response_content = response['output']['choices'][0]['message']['content']
    #     # 在页面上显示模型生成的回复
    #     with st.chat_message("assistant"):
    #         st.markdown(response_content)
    #
    #     # 将模型的输出加入到历史信息中
    #     # TODO 需要修改
    #     st.session_state.history.append(generate_session('assistant', response_content))
    #     st.session_state.history
    #     # 只保留十轮对话，这个可根据自己的情况设定，我这里主要是会把history给大模型，context有限，轮数不能太多
    #     if len(st.session_state.history) > 20:
    #         st.session_state.messages = st.session_state.messages[-20:]
    #
    # else:
    #     st.session_state.history.pop()
    #     st.session_state.history