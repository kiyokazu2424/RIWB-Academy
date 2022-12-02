"""View,Mixinのimport"""
# 認証機能View
from django.contrib.auth.views import (LoginView, LogoutView,PasswordChangeView, PasswordChangeDoneView,
PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
# CRUD処理のView
from django.views.generic import TemplateView,CreateView,DetailView,UpdateView,FormView
# ログインしたユーザーのみの閲覧制限、アクセス可能ユーザーの制限、複数クラス継承時には引数の一番目に持ってこないと不具合の可能性あり
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
"""Model,Formからのimport"""
# Form
from .forms import (LoginForm,UserCreateForm,UserUpdateForm,MyPasswordChangeForm,
MyPasswordResetForm, MySetPasswordForm,EmailChangeForm)
# Model
from .models import User
"""登録時メールなどのためのimport"""
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
"""画面遷移のimport"""
from django.template.loader import render_to_string
from django.shortcuts import redirect,resolve_url
from django.urls import reverse_lazy
"""その他import"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import JsonResponse
from django.shortcuts import render
from .forms import return_major_by_college

"""依存チェーン作成のための関数"""
def getMajor(request):
    "選択された大学をAjaxで受け取り、学部をテンプレに返す"
    # post中のcollegeデータを取得
    college = request.POST.get('college')
    # 選択された大学により学部を取得
    colleges = return_major_by_college(college)
    return JsonResponse({'colleges':colleges})

"""プロジェクトで使用しているUserモデルを取得、処理を書きやすくする"""
user_model = get_user_model()

"""Mixin"""
class OnlyYouMixin(UserPassesTestMixin):
    "ユーザー検査（本人のみしかアクセスできない）機能のクラス"
    # 下の条件を満たさないときに403ページに移動させるかのフラグ、Falseにしたときはログインページへ移動させる
    raise_exception = True
    # 条件としてログイン中のユーザーとアクセスしたユーザーページのpkの一致もしくは、アクセスしたのがスーパーユーザーである
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

"""View"""
# forms.pyからフォームを使用して、クラスとしてviewを定義している
# TemplateViewクラスを使用したViewクラスの作成
class Top(TemplateView):
    "アプリのトップページ"
    template_name = "account/top.html"

class Fee(TemplateView):
    "料金ページ"
    template_name = "account/about_fee.html"

class Login(LoginView):
    "ログインページ"
    template_name = "account/login.html"
    form_class = LoginForm

class Logout(LoginRequiredMixin, LogoutView):
    "ログアウトページ、ログアウト処理のみでページ自体はなくトップに戻る"
    template_name = "account/top.html"

# ①ユーザー登録→②ユーザー仮登録完了ページ→メールを見てリンクを押してもらう→③登録完了ページ、登録処理もここをアクセス時に行われる
class UserCreate(CreateView):
    "①ユーザー登録ページ"
    template_name = 'account/user_create.html'
    form_class = UserCreateForm

    # def get(self,request,*args,**kwargs):
    #     form  = UserCreateForm()
    #     context = super().get_context_data(*args,**kwargs)
    #     context['form'] = form
    #     return render(request, 'address.html', context)
 
    # def post(self,request,**kwargs):
    #     form  = UserCreateForm(request.POST)
    #     if form.is_valid():
    #         selected_province = request.POST['major']
    #         obj = form.save(commit=False)
    #         obj.state = selected_province
    #         obj.save()

    # フォームの内容が有効な時に発動するのがform_valid
    def form_valid(self, form):
        "仮登録メールを発行し、仮登録完了ページにリダイレクト"
        # is_active属性により仮登録と本登録の切り替え、退会手続きなどを制御
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        # メール作成時のテンプレートに必要な内容をまとめる
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            # settings.py中のSECRET_KEYなどから生成される文字列token、user.pkとして作成される。これをもとに本登録URLを作成しメールで送信する
            'token': dumps(user.pk),
            'user': user,
        }
        # 指定フォルダからメールのテンプレートを取得し格納、上がメールの題名、下が本文
        subject = render_to_string('account/mail_template/create/subject.txt', context)
        message = render_to_string('account/mail_template/create/message.txt', context)
        # Userモデルのメール送信メソッド、宛先はモデル中のメールフィールド
        user.email_user(subject, message)
        return redirect('account:user_create_done')

class UserCreateDone(TemplateView):
    "②ユーザー仮登録完了ページ"
    template_name = 'account/user_create_done.html'

class UserCreateComplete(TemplateView):
    "③メール内URLアクセス後のユーザー本登録ページ"
    template_name = 'account/user_create_complete.html'

    # 有効期限の設定、1時間以内でないとURLが無効になる
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60)

    def get(self, request, **kwargs):
        "本登録施行処理をgetにオーバーライドで追加"
        # tokenが正しければ本登録
        token = kwargs.get('token')
        # エラーとならなかった場合、変数user_pkにuser.pkを復号化して格納
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)
        # 期限切れ(期限は上で1時間に設定している)
        except SignatureExpired:
            return HttpResponseBadRequest()
        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()
        # try成功後、tokenは問題なし
        else:
            try:
                user = user_model.objects.get(pk=user_pk)
            except user_model.DoesNotExist:
                return HttpResponseBadRequest()
            # try成功後
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)
        return HttpResponseBadRequest()

class UserDetail(OnlyYouMixin,DetailView):
    "ユーザー情報一覧ページ"
    template_name = 'account/user_detail.html'
    # 閲覧対象モデル指定
    model = user_model

class UserUpdate(OnlyYouMixin,UpdateView):
    "ユーザー情報更新ページ"
    template_name = 'account/user_update.html'
    form_class = UserUpdateForm
    # 更新対象モデル指定
    model = user_model

    # 任意のコンテクストを渡す、superを呼び出し元々のcontextを失わずに済む
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # 元ページ情報を追加
        context['from_page'] = 'update'
        context['message']   = 'ユーザー情報が更新されました'
        return context

    # UpdateViewのメソッドの一部を上書き、更新実行後ユーザ詳細ページへ移動、form_validの最後に呼び出される、putをメゾットに指定してもpostと同じ処理がなされる
    def get_success_url(self):
        message = 'ユーザー情報が更新されました'
        # resolve_urlはurlを文字列で返す、redirectは指定したurlまたはviewを転送
        return resolve_url('account:user_detail', pk=self.kwargs['pk'])

class PasswordChange(LoginRequiredMixin,PasswordChangeView):
    "パスワード変更ページ"
    template_name = 'account/password_change.html'
    form_class = MyPasswordChangeForm
    # 変更成功時のリダイレクト
    success_url = reverse_lazy('account:password_change_done')

class PasswordChangeDone(PasswordChangeDoneView):
    "パスワード変更完了ページ"
    template_name = 'account/password_change_done.html'

# ①メールアドレス変更ページ→②メールアドレスの変更メールを送信ページ→メールからURLを踏む→メールアドレス変更URLページ
class EmailChange(LoginRequiredMixin,FormView):
    "メールアドレス変更ページ"
    template_name = 'account/email_change_form.html'
    form_class = EmailChangeForm

    # フォームの内容が有効な時に発動するのがform_valid
    def form_valid(self, form):
        "変更後のメールアドレスにメール送信"
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }
        # 指定フォルダからメールのテンプレートを取得し格納、上がメールの題名、下が本文
        subject = render_to_string('register/mail_template/email_change/subject.txt', context)
        message = render_to_string('register/mail_template/email_change/message.txt', context)
        # 変更後メールアドレスへ送信
        send_mail(subject, message, None, [new_email])
        return redirect('account:email_change_done')

class EmailChangeDone(TemplateView):
    "②メールアドレスの変更メールを送信完了ページ"
    template_name = 'account/email_change_done.html'

class EmailChangeComplete(TemplateView):
    "③メールアドレス変更URLページ"
    template_name = 'account/email_change_complete.html'

    # 有効期限の設定、1時間以内でないとURLが無効になる、デフォルトは1日以内
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60)
    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()
        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()
        # tokenは問題なし
        else:
            user_model.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)

# ①パスワードを忘れた方ページ→②パスワード変更URL送信完了ページ→メールからURLを踏む→③新パスワード入力ページ→④新パスワード設定完了ページ
class PasswordReset(PasswordResetView):
    "①パスワードを忘れた方ページ、パスワード変更URLをメールで送信"
    template_name = 'account/password_reset_form.html'
    # 使用フォーム指定
    form_class = MyPasswordResetForm
    # 指定フォルダからメールのテンプレートを取得し格納、上がメールの題名、下が本文
    subject_template_name = 'account/mail_template/change/subject.txt'
    email_template_name = 'account/mail_template/change/message.txt'
    # メール送信が成功したらリダイレクト
    success_url = reverse_lazy('account:password_reset_done')

class PasswordResetDone(PasswordResetDoneView):
    "②パスワード変更用URL送信完了ページ"
    template_name = 'account/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    "③新パスワード入力ページ"
    template_name = 'account/password_reset_confirm.html'
    form_class = MySetPasswordForm

    success_url = reverse_lazy('account:password_reset_complete')

class PasswordResetComplete(PasswordResetCompleteView):
    "④新パスワード設定完了ページ"
    template_name = 'account/password_reset_complete.html'
