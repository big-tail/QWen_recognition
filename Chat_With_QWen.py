from http import HTTPStatus
import requests
import dashscope
import json


# TODO 拆分相应包信息


### 处理图片，根据来源生成对应的api消息格式
def dispose_input_to_message(role, user_input, images=None):
    if images is None:
        images = []
    content = [{'text': user_input}]
    for image in images:
        content.append({"image": image})
    messages = {
        'role': role,
        'content': content
    }
    return messages


### 侦测网络图片是否存在
def check_online_image_exist(image_url):
    try:
        r = requests.get(image_url)
        return r.status_code

    except:
        return 'Image does not exist!'


### 本地图片上传接口
def conversation_call_with_sdk(messages, model='qwen-vl-plus', api_key='sk-ac227686a13348d9a5fcf3857c36de48'):
    dashscope.api_key = api_key
    response = dashscope.MultiModalConversation.call(model,
                                                 messages=messages)
    return response


### 网络图片URL上传接口
def conversation_call_with_http(messages, model='qwen-vl-plus', api_key='sk-ac227686a13348d9a5fcf3857c36de48'):
    model_url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'

    headers = {'Content-Type': 'application/json',
               'Authorization': api_key}
    payload = {
        'model': model,
        'input': {
            'messages': messages
        }
    }
    print(payload)
    response = requests.request("POST", model_url, headers=headers, data=json.dumps(payload))
    return response


### 拆分响应包信息
def dispose_response_message(response):
    status_code = response.status_code
    try:
        response = json.loads(response.text)
    except Exception as e:
        print(f'响应包错误，{e.__class__.__name__}:{e}')
    if status_code == HTTPStatus.OK:
        message = response['output']['choices'][0]['message']
    else:
        # 完成错误代码输出
        error_code = response['code']
        error_message = response['message']
        message = f'响应码:{status_code} 错误详细信息{error_message}'
        print(message)
    return status_code, message
