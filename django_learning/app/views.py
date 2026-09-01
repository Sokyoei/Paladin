import json
import time

from django.http import HttpRequest, StreamingHttpResponse
from django.shortcuts import render


def root(request: HttpRequest):
    return render(request, 'index.html')


def index(request: HttpRequest):
    return render(request, 'app/index.html')


def sse_view(request: HttpRequest):
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
