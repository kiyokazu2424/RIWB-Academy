from django.urls import path
from . import views

app_name = 'account'
# views.pyからビューを引き継ぎ、urlに沿って反映
urlpatterns = [
    # ルートパス、トップページ
    path("", views.Top.as_view(), name="top"),
    # 料金案内ページ
    path("acount/about_fee", views.Fee.as_view(), name="fee"),
    # ログインページ
    path("account/login/", views.Login.as_view(), name="login"),
    # ログアウトページ
    path("account/logout/", views.Logout.as_view(), name="logout"),
    # 新規登録ページ
    path('account/user_create/', views.UserCreate.as_view(), name='user_create'),
    # 仮登録完了ページ
    path('account/user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    # 本登録ページ
    path('account/user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    # ユーザー情報閲覧ページ
    path('account/user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    # ユーザー情報更新ページ
    path('account/user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    # パスワード変更ページ
    path('account/password_change/', views.PasswordChange.as_view(), name='password_change'),
    # パスワード変更完了ページ
    path('account/password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    # パスワードリセットページ(忘却時用)
    path('account/password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    # パスワードリセット完了ページ
    path('account/password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    # 新パスワード作成ページ
    path('account/password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    # 新パスワード作成完了ページ
    path('account/password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('account/email/change/', views.EmailChange.as_view(), name='email_change'),
    path('account/email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('account/email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),
    
]