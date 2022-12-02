from django.urls import path
from . import views

app_name = 'study'
# views.pyからビューを引き継ぎ、urlに沿って反映
urlpatterns = [
    # ルートパス、トップページ
    path("", views.Study.as_view(), name="study"),
    # ジャンル作成ページ
    path("genre_create", views.GenreCreate.as_view(), name="genre_create"),
    # ジャンル詳細ページ、pkはジャンルのid
    path("genre/<int:pk>", views.GenreDetail.as_view(), name="genre_detail"),
    # 教材作成ページ
    path("text_create", views.TextCreate.as_view(), name="text_create"),
    # 教材詳細ページ、pkは教材のid
    path("text/<int:pk>", views.TextDetail.as_view(), name="text_detail"),
    # コメント作成、ページ自体は存在せず、教材詳細ページでコメント投稿、pkはコメントしたい動画のid
    path("comment_create/<int:pk>", views.CommentCreate.as_view(), name="comment_create"),
    # スレッド作成、ページ自体は存在せず、教材詳細ページでスレッド投稿、pkはスレッドを作りたい動画のid
    path("thread_create/<int:pk>", views.ThreadCreate.as_view(), name="thread_create"),
    # スレッド詳細ページ、pkはスレッドのid
    path("thread/<int:pk>", views.ThreadDetail.as_view(), name="thread_detail"),
    # 返信作成、ページ自体は存在せず、スレッド詳細ページで返信投稿、pkは返信を作りたいスレッドのid
    path("reply_create/<int:pk>", views.ReplyCreate.as_view(), name="reply_create"),
    # 自己分析一覧ページ
    path("analysis", views.Analysis.as_view(), name="analysis"),
    # エニアグラム診断ページ
    path("enneagram", views.Enneagram.as_view(), name="enneagram"),
    # エニアグラム診断結果ページ
    path("enneagram_result", views.EnneagramResult.as_view(), name="enneagram_result"),


]