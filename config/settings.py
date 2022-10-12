"""注意事項"""
# 本番環境では、各base.htmlの{% load cdnstaticfiles %}を無効にする、vueの本番環境の方にする
# また、DEBUGとDATABASEを入れ替える、DEBUGがTrueだとエラーの内容がブラウザに表示される、脆弱性があるなど。DATABASEはバージョン管理外としている
# セキュリティーの観点から、バージョン管理外のlocal_settingsにSECRET_KEY,DATABASE,メールなどの設定を記述しインポートしてある、本番でもEC2のマシーンに対して追加で作成する。
# macの方でなぜかmysqlclientが使用できないバグがあるぽいのでpymysqlを使用してるがec2では使わない
"""他ファイルなどからのインポート"""
import os
#機密度の高い情報の設定、ログに必要なミドルウェアはlocal_settings、orig_logにまとめてここで使用
from .local_settings import *
from .orig_log import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.(riwb_academy/のこと)
# BASE_DIR = Path(__file__).resolve().parent.parent

# プロジェクトのドキュメントルート（一番上のprojectディレクトリ）のパス
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

"""静的ファイル、アップロードファイルのディレクトリ"""
# staticファイル設定
STATIC_URL = '/static/'
# 開発環境
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# 本番環境の静的ファイルの集める先をproject直下に設定（manage.py collectstaticコマンドにより集めることができる）
STATIC_ROOT = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = f'/var/www/{BASE_DIR.name}/static'

# mediaファイル設定（画像、動画などのファイルアップロード機能で必要）
MEDIA_URL = '/media/' # ブラウザからアクセスする際のアドレス
# 開発環境
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # 画像ファイルの保存ディレクトリ
# 本番環境（リバースプロキシで配信）
# MEDIA_ROOT = f'/var/www/{BASE_DIR.name}/media'

"""使用アプリ、ミドルウェア、テンプレートなどの指定"""
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',# session
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # フォーム装飾に使う
    'widget_tweaks',
    # キャッシュの無効化（開発用、{% load cdnstaticfiles %}をつける）
    'django_cachekiller',
    # ログイン回数などに制限をかける
    'axes',
    # ストレージ管理
    'storages',
    # ファイルアップロードのフィールドのストレージからの自動削除
    'django_cleanup.apps.CleanupConfig',

    # アプリの追加
    'config',
    'account',
    'study',
]

# リクエストとレスポンスの間に入って処理を行うモジュール
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',# session有効
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',# axes、追加位置は最後が良い
    # 'middleware.orig_log.CustomAttrMiddleware',# オリジナルのログミドルウェア
]

# リクエストを受けた際に初めに呼び出すファイル名、基本的にデフォルトのurls.pyで問題ない
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


"""ログインセキュリティー"""
# パスワード作成時に強固なパスワードでないと登録できないようにする（デフォルト）、
# また、AbstractBaseUserを使用してるのでパスワードは平文を避けて登録される
AUTH_PASSWORD_VALIDATORS = [
    {
        # username,first_name,last_nameと一致していないか
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # 8文字以上
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # よくあるパスワードのリストの要素と一致していないか
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # 数値のみで構成されていないか
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        # 大文字、小文字、数値を含むか（自作で追加）
        'NAME': 'config.pass_validation.CustomValidator',
    },
]

# ログイン回数などの設定
# axesの設定として必要
AUTHENTICATION_BACKENDS = [
'axes.backends.AxesBackend',
'django.contrib.auth.backends.ModelBackend',
]

# ログインに5回失敗するとアカウントがロックされる
AXES_FAILURE_LIMIT  = 5
# ロックの解除時間、8時間に設定
AXES_COOLOFF_TIME = 8
# Trueならユーザー名でログイン失敗をカウント、FalseならIPアドレスによりカウント
AXES_ONLY_USER_FAILURES = False
# ログインに成功したとき、カウントをリセット
AXES_RESET_ON_SUCCESS = True
# ロック時に表示するテンプレート
AXES_LOCKOUT_TEMPLATE = 'axes_locked.html'
# 以下のコマンドでロックは解除できる
# python manage.py axes_reset

"""日時"""
# 修正前 LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ja'
# 修正前 TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""ログイン"""
AUTH_USER_MODEL = 'account.User' # カスタムしたユーザーモデルをデフォルトに設定
LOGIN_URL = "account:login"      # ログイン必要画面へ遷移時に、ログインしてない時のリダイレクト先、ログイン画面にリダイレクト
LOGIN_REDIRECT_URL = "study:study"      # ログイン後のリダイレクト先
LOGOUT_REDIRECT_URL = "account:top"      # ログアウト後のリダイレクト先

# ログ系
# formatters:ログに出力されるときの形式指定、出力できるものはデフォルトで用意されている
# filter:ログレベルとは別に、ブール関数型でフィルタを設定
# handlers:ロガーが実行されたときの振る舞い、出力場所などの指定
# loggers:アプリからログ操作を行うためのロガーオブジェクトの設定
# ログレベルについてCRITICAL>ERROR>WARNING>INFO>DEBUG>NOTSET、どの程度のものまでログを見たいかによって設定
# LOGGING = {
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s '
#                       '%(process)d %(thread)d user=%(user)s %(message)s'
#         },
#     },
#     'filters' : {
#         'custom': {
#             '()': 'middleware.custom_logging.CustomAttrFilter'
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#             'filters': ['custom']
#         },
#     },
# }

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,

#     'formatters': {
#         # 時間、レベル、httpメソッド、url、ステータスなどを羅列するフォーマット
#         'format1': {
#             'format': '%(asctime)s [%(levelname)s] %(process)d %(thread)d '
#                       '%(pathname)s:%(lineno)d %(message)s'
#         },
#     },

#     'handlers': {
#         # 出力先として、コンソール、ファイル、メールなどがある
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'when': 'D',
#             'interval': 1,
#             'backupCount': 7,
#             # ログのファイルパス
#             'filename': 'app.log',
#             'formatter': 'format1',
#         },
#         'console': {
#             'level': 'INFO',
#             'class': 'logging.StreamHandler',
#             'formatter': 'format1',
#         },
#     },

#     'loggers': {
#         # djangoのデフォルト、いじらない
#         'django': {
#             'handlers': ['console', 'file'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#         # このアプリ上での設定
#         'riwb_academy': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     }

# }

# ec2ではhandlersのfileがうまくいかないため一旦除外した
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        # 時間、レベル、httpメソッド、url、ステータスなどを羅列するフォーマット
        'format1': {
            'format': '%(asctime)s [%(levelname)s] %(process)d %(thread)d '
                      '%(pathname)s:%(lineno)d %(message)s'
        },
    },

    'handlers': {
        # 出力先として、コンソール、ファイル、メールなどがある
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'format1',
        },
    },

    'loggers': {
        # djangoのデフォルト、いじらない
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # このアプリ上での設定
        'riwb_academy': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }

}