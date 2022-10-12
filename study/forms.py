from django import forms
from .models import Genre,Text,Comment,Thread,Reply

class GenreForm(forms.ModelForm):
    """ジャンルフォーム（スーパーユーザーのみ利用可能）"""
    class Meta:
        # どのモデルをフォームにするか指定
        model = Genre
        # そのフォームの中から表示するフィールドを指定
        fields = ('name', 'description', 'thumbnail')
        labels={'name':'ジャンル名', 'description':'概要説明文', 'thumbnail':'サムネイル'}

    # フォームを綺麗にするための記載
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class TextForm(forms.ModelForm):
    """教材フォーム（スーパーユーザーのみ利用可能）"""
    class Meta:
        # どのモデルをフォームにするか指定
        model = Text
        # そのフォームの中から表示するフィールドを指定
        fields = ('title', 'description', 'thumbnail', 'text', 'genre_id')
        labels={'title':'タイトル', 'description':'概要説明文', 'thumbnail':'サムネイル', 'text':'教材ファイル', 'genre_id':'ジャンル'}

    # フォームを綺麗にするための記載
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CommentForm(forms.ModelForm):
    """コメントフォーム（各教材の詳細ページで利用可能）"""
    class Meta:
        model = Comment
        fields = ('comment',)
        labels = {'comment':'コメント',}

    # フォームを綺麗にするための記載
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ThreadForm(forms.ModelForm):
    """スレッドフォーム（各教材の詳細ページで利用可能）"""
    class Meta:
        model = Thread
        fields = ('title','message')
        labels = {'title':'スレッドのタイトル','message':'スレッドの内容'}

    # フォームを綺麗にするための記載
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ReplyForm(forms.ModelForm):
    """リプライフォーム（各スレッドの詳細ページで利用可能）"""
    class Meta:
        model = Reply
        fields = ('reply',)
        labels = {'reply':'メッセージ返信',}

    # フォームを綺麗にするための記載
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
