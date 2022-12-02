from django import forms
# AuthenticationFormには標準でユーザー名とパスワードのフォームが定義されている
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
# ユーザーモデルの取得関数
from django.contrib.auth import get_user_model
# メールアドレスバリデーションの際に使用
from django.core.exceptions import ValidationError
# 学部学科のデータ選択肢に使用
import json

"""依存チェーンドロップダウンフォームのための関数"""
def readJson(filename):
    "jsonの読み込み関数"
    with open(filename, 'r',encoding="utf-8_sig") as fp:
        return json.load(fp)

 
def get_college():
    "大学名を選択するタプルの作成"
    filepath = './static/account/json/kokuritu.json'
    all_data = readJson(filepath)
    colleges = list(all_data.keys())
    all_colleges = [('-----','---大学の選択---')]
    for college in colleges:
        all_colleges.append((college,college))
    return all_colleges
 
 
def return_major_by_college(college):
    "大学の選択を取得しそこの学部を取得"
    filepath = './static/account/json/kokuritu.json'
    all_data = readJson(filepath)
    #指定の都道府県の市区町村データを取得
    all_majors = all_data[college]
    return all_majors

"""プロジェクトで使用しているUserモデルを取得、処理を書きやすくする"""
User = get_user_model()

class LoginForm(AuthenticationForm):
    "ログインフォーム"
    def __init__(self, *args, **kwargs):
        "継承元の初期化"
        super().__init__(*args, **kwargs)

        # Djangoのフォームについて{{field.label}}は文字列、{{field}}はinputタグなので前者はdivタグで囲む
        for field in self.fields.values():
            # プレースフォルダにフィールドのラベルを入れる
            field.widget.attrs['placeholder'] = field.label 
            # {{filed}}により生成されるinputタグに対してクラスが追加される、全フォーム共通
            field.widget.attrs['class'] = 'form-input'

class UserCreateForm(UserCreationForm):
    "新規登録フォーム"
    class Meta:
        # 使用するモデルの指定
        model = User
        # 表示するフィールド、ラベル(ラベルにはデフォルトがある)の指定、'__all__'で全てを指定、pass1,2はパスワードとその確認
        fields = ['email','password1','password2','first_name','last_name','job']
        labels = {'email':'メールアドレス','first_name':'苗字','last_name':'名前','job':'職業'}
        # fields = '__all__'

    # フィールドカスタマイズ
    def __init__(self, *args, **kwargs):
        # 継承元の初期化
        super().__init__(*args, **kwargs)

        # Metaクラスの指定fieldを利用し各種フィールドを設定
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label 
            field.widget.attrs['class'] = 'form-input'

    def clean(self):
        "新規登録時九大のメールアドレス以外受け付けない"
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if email:
            if "@s.kyushu-u.ac.jp" not in email:
                raise ValidationError(("九大のメールアドレス以外使用できません。"),code="require kyudai email")

    def clean_email(self):
        "本登録を忘れリンク切れが起きる、他人が手違いで自分のメアドを使用するなどで、二度同じアドレスを使えないため登録できなくなることの回避"
        email = self.cleaned_data['email']
        # 仮登録アカウントの削除
        User.objects.filter(email=email, is_active=False).delete()
        return email

class UserUpdateForm(forms.ModelForm):
    "ユーザー情報更新フォーム"

    class Meta:
        model = User
        # 詳細ページにて更新可能な項目
        fields = ('last_name', 'first_name','job')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label 
            field.widget.attrs['class'] = 'form-input'

class MyPasswordChangeForm(PasswordChangeForm):
    "パスワード変更フォーム"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # フィールドラベルの変更
        self.fields['old_password'].label  = '現在のパスワード'
        self.fields['new_password2'].label = '新しいパスワード（確認）'

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label 
            field.widget.attrs['class'] = 'form-input'

class MyPasswordResetForm(PasswordResetForm):
    "パスワード忘れたときのフォーム"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label 
            field.widget.attrs['class'] = 'form-input'


class MySetPasswordForm(SetPasswordForm):
    "パスワード再設定用フォーム(パスワード忘れて再設定)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label 
            field.widget.attrs['class'] = 'form-input'

class EmailChangeForm(forms.ModelForm):
    "メールアドレス変更フォーム"

    class Meta:
        model = User
        fields = ('email',)
        labels = {'email':'新しいメールアドレス'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label 
            field.widget.attrs['class'] = 'form-input'

    def clean_email(self):
        "仮登録状態で同じメールアドレスのアカウントを削除"
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email