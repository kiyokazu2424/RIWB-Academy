# from storages.backends.s3boto3 import S3Boto3Storage


# class MediaStorage(S3Boto3Storage):
#     location = 'media'  # /media というURLで配信
#     file_overwrite = False  # 同名ファイルは上書きせずに似た名前のファイル

# settings中でgitに上げたくないものをlocal_settingsに書く、settingsにインポートする、このファイルはgitignore

# ユーザーが入力したパスワードをDBに保存する前に暗号化する際使われる
"""基本のセキュリティー"""
SECRET_KEY = 'django-insecure-=mh1esp3-0=hsqm%uxh(5e=csyoy@f$w*+tm)hby!h2f)d!w!v'

# 開発環境
DEBUG = True
# 本番環境
# DEBUG = False

# httpでアクセスされた時httpsに自動リダイレクト
# 開発環境
SECURE_SSL_REDIRECT = False
# 本番環境
# SECURE_SSL_REDIRECT = True

# Djangoがアクセスを受けるIPアドレスを指定、開発中は'*'でも問題ない。本番ではローカルホストと本番環境用、EC2のパブリックIPアドレス、リモートホスト、紐付けたドメイン。
ALLOWED_HOSTS = ['127.0.0.1','43.206.47.103','ec2-43-206-47-103.ap-northeast-1.compute.amazonaws.com','riwb-academy.com']

"""セッション関連"""
# 管理はcookieベースでURL埋め込みはなし、ID自体もランダムに発行LoginViewではログイン成功時にセッション更新
# CookieにSecure属性を付与
# 開発環境
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_HTTPONLY = False
# SESSION_COOKIE_HTTPONLY = False
# 本番環境
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
# SESSION_COOKIE_HTTPONLY = True
# セッションの保存先、DB,キャッシュ,ファイル、クッキーなどがある、今回はDBにしている
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

"""データベース"""
# 開発環境
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'riwb_academy',
        'USER': 'root',
        'PASSWORD': 'Riwb_1111',
        'HOST':'localhost',
        'PORT':'3306',
    }
}

# 本番環境
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'academy',
#         'USER': 'Riwb',
#         'PASSWORD': 'Riwb2424',
#         'HOST':'academy-database.crydgdidi19c.ap-northeast-1.rds.amazonaws.com',
#         'PORT':'3306',
#     }
# }

"""メール送信元の接続設定"""
# gmail
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'riwb.tech@gmail.com'
EMAIL_HOST_PASSWORD = 'myapmeenywbvlqid'

# conoha
# EMAIL_HOST = 'mail30.conoha.ne.jp'
# EMAIL_PORT = 465 # SSL有効時のsmtpポート
# EMAIL_HOST_USER = 'academy@riwb.org'
# EMAIL_HOST_PASSWORD = 'RIWBtech20220617#'

# メール送信時の暗号化
EMAIL_USE_TLS = True

# コンソールで確認したいときの設定
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# 実際メールを送るときの設定
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

"""ストレージ関連の設定"""
# 本番環境
# AWS_ACCESS_KEY_ID = 'AKIAZ56KECZ4VRRQSUFR'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_STORAGE_BUCKET_NAME = 'riwb-academy'

# 今回はstaticのものはec2、mediaのものをS3にアップ
# 動画、ジャンルの画像など
# AWS_LOCATION = 'media'
# メディアファイルの設定
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# 見本、ずっとオフ
# デフォルト、よくある設定パターン
# 静的ファイルの設定
# AWS_LOCATION = 'static'
# 静的ファイルストレージクラス、django-storagesにあるS3Boto3Storageを使用、settingsのAWS_LOCATIONを参照するので、urlは/staticとなる
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# メディアファイルの設定、静的ファイルと別クラスのストレージを作成し使用、同名ファイルの上書きを防ぐため
# DEFAULT_FILE_STORAGE = 'riwb-academy.backends.MediaStorage'
