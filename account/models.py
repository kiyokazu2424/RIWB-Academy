from cProfile import label
from dis import COMPILER_FLAG_NAMES
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# デフォルトのユーザーモデルではユーザー名(id)をemailに出来ないのでカスタムしている
# ユーザー新規登録時のヘルパー関数、元々UserManagerがありそれをカスタムしている
class CustomUserManager(UserManager):
    "ユーザーマネージャー"
    use_in_migrations = True

    # emailとpasswordは必須でその他は任意でつけられる
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        # emailの前後から空白をとり、末尾から初めての@でname,domainに分割domainを小文字にしてくっつけemailとして出力
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 上記の関数を利用し実行するユーザー作成関数を作成
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    # 管理者作成
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

# 実際に登録するユーザーモデル
class User(AbstractBaseUser, PermissionsMixin):
    "カスタムユーザーモデル."
    # 選択肢フォームの選択肢
    job_choices = ((0,'小学生以下'),(1,'中学生'),(2,'高校生'),(3,'大学生(学部生)'),
    (4,'大学生(修士生)'),(5,'大学生(博士生)'),(6,'社会人'),(7,'その他'))

    # 各種dbの項目、パスワードはデフォルトでAbstractBaseUserに入っている
    # 入力してもらう(表示する)項目
    email      = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name  = models.CharField(_('last name'), max_length=30, blank=True)

    # 区分
    job          = models.IntegerField(_('job'), choices=job_choices,default=7,null=True)
    # 大学名
    # college    = models.IntegerField(_('college'), choices=job_choices,default=0,null=True)
    # # 学部名
    # faculty    = models.IntegerField(_('faculty'), choices=job_choices,default=0,null=True)
    # # 学科名
    # department = models.IntegerField(_('department'), choices=job_choices,default=0,null=True)

    # デフォルトを決めており、ユーザー側がいじらない項目
    # スタッフ
    is_staff = models.BooleanField(_('staff status'),default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    # アカウント状態
    is_active = models.BooleanField(_('active'),default=True,
        help_text=_(
            'Designates whether this user should be treated as active.'
            'Unselect this instead of deleting accounts.'
           ),
    )
    # 登録日
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # 上のクラスを導入
    objects = CustomUserManager()

    # 主キーであるUSERNAME_FIELDにemailを指定
    EMAIL_FIELD     = 'email'
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    # Metaという内部クラスを作成し、djangoのモデルの取り扱い方法を変更する
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        "Return the first_name plus the last_name, with a space in between."
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Return the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        "Send an email to this user."
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        "username属性のゲッター他アプリケーションが、username属性にアクセスした場合に備えて定義メールアドレスを返す"

        return self.email