from http import HTTPStatus
import requests
import dashscope
import json

# TODO 拆分相应包信息
def show_message_box(*args):
    pass


# 本地图片上传接口
def conversation_call_with_sdk(messages):
    response = dashscope.MultiModalConversation.call(model='qwen-vl-plus',
                                                     messages=messages)
    return response


# 网络图片URL上传接口
def conversation_call_with_http(messages):
    model_url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'

    headers = {'Content-Type': 'application/json',
               'Authorization': 'sk-ac227686a13348d9a5fcf3857c36de48'}
    payload = {
        'model': 'qwen-vl-plus',
        'input': {
            'messages': messages
        }
    }
    print(payload)
    response = requests.request("POST", model_url,headers=headers,data=json.dumps(payload))
    return response

# 拆分响应包信息
def dispose_response_message(response):
    status_code = response.status_code
    response = json.loads(response.text)
    if status_code == HTTPStatus.OK:
        message = response['output']['choices'][0]['message']
    else:
        message = ''
        error_code = response['code']
        error_message = response['message']
    return status_code, message
