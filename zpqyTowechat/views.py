from django.shortcuts import render

from django.http import HttpResponse
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import WeChatClient
from wechatpy.messages import TextMessage
from wechatpy.replies import TextReply
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# 你的Token和AES Key
TOKEN = 'your_token'
APPID = 'your_appid'
APPSECRET = 'your_appsecret'

client = WeChatClient(APPID, APPSECRET)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def wechat(request):
    signature = request.GET.get('signature', '')
    timestamp = request.GET.get('timestamp', '')
    nonce = request.GET.get('nonce', '')
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        return HttpResponseBadRequest('Invalid signature')

    if request.method == 'GET':
        return HttpResponse(request.GET.get('echostr', ''))

    # 解析微信服务器发送过来的消息
    message = client.parse_message(request.body)

    if isinstance(message, TextMessage):
        # 调用智谱清言API获取回复
        reply_content = get_zhipu_reply(message.content)
        reply = TextReply(content=reply_content, message=message)
        return HttpResponse(reply.render(), content_type="application/xml")
    else:
        return HttpResponse('')

def get_zhipu_reply(question):
    # 这里替换为调用智谱清言API的代码
    # 假设返回的是字符串
    return "这是智谱清言的回复"
