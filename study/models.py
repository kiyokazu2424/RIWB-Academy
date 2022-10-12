from email.policy import default
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from account.models import User

# idは自動で作成されるがあえて明記
# FileField,ImageFieldのupload_toはMEDIA_URLから見たもの

class Genre(models.Model):
  """教材のジャンル"""
  # id（主キー）
  id = models.AutoField(primary_key=True)
  # ジャンル名
  name = models.CharField(max_length=32, default="")
  # 概要説明
  description = models.TextField(max_length=100,default='No description')
  # サムネイル画像
  thumbnail = models.ImageField(upload_to='genre/', 
      validators=[FileExtensionValidator(allowed_extensions=['png','jpeg'])],null=True, blank=True)
  # アップロード日
  upload_date = models.DateTimeField(default=timezone.now)

class Text(models.Model):
  """動画など教材"""
  # id（主キー）
  id = models.AutoField(primary_key=True)
  # コンテンツ名
  title = models.CharField(max_length=32)
  # 概要説明
  description = models.TextField(max_length=100,default='No description')
  # サムネイル画像
  thumbnail = models.ImageField(upload_to='text/img',
      validators=[FileExtensionValidator(allowed_extensions=['png','jpeg'])],null=True, blank=True)
  # 教材ファイル
  text = models.FileField(upload_to='text/textfile',
      validators=[FileExtensionValidator(allowed_extensions=['MOV','MPEG4','mp4'])],default='')
  # アップロード日
  upload_date = models.DateTimeField(default=timezone.now)
  # ジャンルid、所属するジャンルが消えた時一緒に消える、textsという名前で逆参照できるようにする
  genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE,related_name="texts",to_field="id")

class Comment(models.Model):
  """各教材に対するコメント"""
  # id（主キー）
  id = models.AutoField(primary_key=True)
  # コメント文
  comment = models.TextField(max_length=200,default='')
  # 教材id、所属する教材が消えた時一緒に消える、commentsという名前で逆参照できるようにする
  text_id = models.ForeignKey(Text, on_delete=models.CASCADE,related_name="comments",to_field="id")
  # ユーザーid、所属するユーザーが消えた時一緒に消える、commentsという名前で逆参照できるようにする
  user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="comments",to_field="id",default='')
  # コメント日
  upload_date = models.DateTimeField(default=timezone.now)

class Thread(models.Model):
  """各教材に対するスレッド"""
  # id（主キー）
  id = models.AutoField(primary_key=True)
  # スレッドタイトル
  title = models.CharField(max_length=32,default='')
  # 話題の詳細文、質問や教材に付随するワードなどの情報、意見交換
  message = models.TextField(max_length=200,default='')
  # 教材id、所属する教材が消えた時一緒に消える、threadsという名前で逆参照できるようにする
  text_id = models.ForeignKey(Text, on_delete=models.CASCADE,related_name="threads",to_field="id")
  # ユーザーid、所属するユーザーが消えた時一緒に消える、threadsという名前で逆参照できるようにする
  user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="threads",to_field="id",default='')
  # 作成日
  upload_date = models.DateTimeField(default=timezone.now)

class Reply(models.Model):
  """各スレッドに対する返信"""
  # id（主キー）
  id = models.AutoField(primary_key=True)
  # 返信文
  reply = models.TextField(max_length=200,default='')
  # スレッドid、所属するスレッドが消えた時一緒に消える、commentsという名前で逆参照できるようにする
  thread_id = models.ForeignKey(Thread, on_delete=models.CASCADE,related_name="replies",to_field="id")
  # ユーザーid、所属するユーザーが消えた時一緒に消える、commentsという名前で逆参照できるようにする
  user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="replies",to_field="id",default='')
  # 返信日
  upload_date = models.DateTimeField(default=timezone.now)
