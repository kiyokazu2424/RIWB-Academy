"""オリジナルのログミドルウェアを書き込むためのファイル"""


import logging
import threading

local = threading.local()

class CustomAttrMiddleware:
    """logに出力するカスタム項目を取得するMiddleware"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """クライアントからのリクエスト時にrequestのusernameを取得してthreading.local()に一時保存"""
        if request.user:
            setattr(local, 'user', request.user.username)
        else:
            setattr(local, 'user', None)

        response = self.get_response(request)

        # response時はクリアしておく
        setattr(local, 'user', None)

        return response

class CustomAttrFilter(logging.Filter):
    """logにカスタム項目（今回はlocal）を出力するためのfilter"""
    def filter(self, record):
        record.user = getattr(local, 'user', None)
        return True