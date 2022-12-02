# formatters:ログに出力されるときの形式指定、出力できるものはデフォルトで用意されている
# filter:ログレベルとは別に、ブール関数型でフィルタを設定
# handlers:ロガーが実行されたときの振る舞い、出力場所などの指定
# loggers:アプリからログ操作を行うためのロガーオブジェクトの設定
# ログレベルについてCRITICAL>ERROR>WARNING>INFO>DEBUG>NOTSET、どの程度のものまでログを見たいかによって設定

# ファイルパスがec2では違うためエラーとなる
import os
# プロジェクト直下のlogディレクトリにログファイルを出力するよう指定
LOG_BASE_DIR = os.path.join("","log")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(asctime)s [%(levelname)s] %(message)s"}},

    "handlers": {
        "info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_BASE_DIR, "info.log"),
            "formatter": "simple",
        },
        "warning": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_BASE_DIR, "warning.log"),
            "formatter": "simple",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_BASE_DIR, "error.log"),
            "formatter": "simple",
        },
    },

    "root": {
        "handlers": ["info", "warning", "error"],
        "level": "INFO",
    },
}

