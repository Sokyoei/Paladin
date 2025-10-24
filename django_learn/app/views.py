import json
import time

from django.http import StreamingHttpResponse
from django.shortcuts import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("hello world")


def sse_view(request):
    """
    Server-Sent Events 视图函数
    返回一个持续的 HTTP 响应，用于向客户端推送实时数据
    """

    def event_stream():
        while True:
            data = {'time': time.strftime('%Y-%m-%d %H:%M:%S'), 'message': 'Hello from SSE!'}
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(1)

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    # response['Connection'] = 'keep-alive'
    response['Access-Control-Allow-Origin'] = '*'
    return response
