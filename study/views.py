"""View,Mixinのimport"""
# CRUDのView
from django.views.generic import TemplateView,CreateView,DetailView
# ログインしたユーザーのみの閲覧制限、アクセス可能ユーザーの制限、複数クラス継承時には引数の一番目に持ってこないと不具合の可能性あり
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
"""Model,Formからのimport"""
# Form
from .forms import GenreForm,TextForm,CommentForm,ThreadForm,ReplyForm
# Model
from .models import User,Genre,Text,Comment,Thread,Reply
"""画面遷移のimport"""
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
"""その他のimport"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os,csv

"""アンケートに使用するcsvファイルの読み込み"""
def read_csv(file_name):
    "エニアグラムのアンケート"
    # 開発環境
    csv_file = open(f"./static/study/csv/{file_name}", "r", encoding="UTF-8", errors="", newline="")
    # 本番環境
    # csv_file = open(f"/home/ec2-user/Django//riwb-academy/static/study/csv/{file_name}", "r", encoding="UTF-8", errors="", newline="")
    # リスト形式で読み込む
    csv_data = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    header = next(csv_data)
    data_lis = []
    for row in csv_data:
        data_lis.append(row)
    return data_lis

"""Mixin"""
class SuperuserRequiredMixin(UserPassesTestMixin):
    "スーパーユーザー以外のユーザーがアクセスした際、403ページを返す機能"
    def test_func(self):
        "スーパーユーザかチェック"
        return self.request.user.is_superuser

"""View"""
# forms.pyからフォームを使用して、クラスとしてviewを定義している
# TemplateViewクラスを使用したViewクラスの作成
class Study(LoginRequiredMixin,TemplateView):
    "学習画面トップページ"
    template_name = 'study/study.html'

    def get(self, request, *args, **kwargs):
        "トップページであり、ジャンルを表示したいのでオーバーライド"
        # 教材ジャンルの取得
        genre_data = Genre.objects.all()
        context = {'genre_data':genre_data}
        return render(request, 'study/study.html',context)

class GenreCreate(SuperuserRequiredMixin,CreateView):
    "ジャンル登録（スーパーユーザーのみアクセス可能）、ログインしていないときはログインページに遷移"
    template_name = 'study/genre_create.html'
    form_class = GenreForm
    model = Genre

    # 投稿に成功した時のURL
    success_url = reverse_lazy('study:study')

    def post(self, request, *args, **kwargs):
        "FileField,ImageFieldの場合formの上書きが必要、postの処理をオーバーライド"
        form = GenreForm(request.POST, request.FILES)
        # formを保存 
        form.save()
        return redirect('study:study')

class GenreDetail(LoginRequiredMixin,DetailView):
    "ジャンルの詳細（教材一覧）ページ"
    template_name = 'study/genre_detail.html'
    model = Genre

    def get(self, request, *args, **kwargs):
        "ジャンルに属する教材をページングするための準備"
        # 表示中のジャンルオブジェクトを取得
        genre_object = Genre.objects.get(pk=self.kwargs.get('pk'))
        # ジャンルに属する教材のオブジェクトたちの取得
        queryset = genre_object.texts.all()
        # ページネーションの処理
        # 一ページあたりのオブジェクト数
        count = 3
        paginator = Paginator(queryset, count)
        # 現在ブラウザに表示しているページ数の取得処理、初回はオブジェクトがある時Noneでtry中の二つ目、ない時emptyなので三つ目が発動
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request,
                     'study/genre_detail.html',
                    {'genre':genre_object,'text_list': page_obj.object_list,
                       'page_obj': page_obj}
                    )


class TextCreate(SuperuserRequiredMixin,CreateView):
    "教材登録（スーパーユーザーのみアクセス可能）、ログインしていないときはログインページに遷移"
    template_name = 'study/text_create.html'
    form_class = TextForm
    model = Text

    # 投稿に成功した時のURL
    success_url = reverse_lazy('study:study')

    def post(self, request, *args, **kwargs):
        "FileField,ImageFieldの場合formの上書きが必要、postの処理をオーバーライド"
        form = TextForm(request.POST, request.FILES)
        # formを保存
        form.save()
        return redirect('study:study')

class TextDetail(LoginRequiredMixin,DetailView):
    "教材の詳細（実際の教材）ページ"
    template_name = 'study/text_detail.html'
    model = Text

    def get_context_data(self, **kwargs):
        "教材詳細ページにおいてコメント、スレッドも作成できるための処理"
        context = super().get_context_data(**kwargs)
        # テンプレートにコメント作成フォーム、スレッド作成フォームを渡す
        context['comment_form'] = CommentForm
        context['thread_form'] = ThreadForm

        # 教材に紐づいたコメント、スレッド数の表示準備、初めに表示中の表示中の教材オブジェクトを取得
        text_object = Text.objects.get(pk=self.kwargs.get('pk'))
        # 外部キーの件数参照はrelated_nameを指定している時その名前でできる、指定してない場合comment_setが使える
        comments = text_object.comments.all()
        comment_num = len(comments)
        threads = text_object.threads.all()
        thread_num = len(threads)

        # コンテキストに追加
        context['comment_num'] = comment_num
        context['thread_num'] = thread_num
        return context

class CommentCreate(CreateView):
    "教材へのコメント作成、ページは表示されず、作成のために必要"
    form_class = CommentForm
    model = Comment

    def form_valid(self, form):
        "フォームが送信された後に、コメントの紐づく教材、ユーザーのidをそれぞれ規定、送信後は教材画面を表示"

        # 登録オブジェクトの取得
        text_pk = self.kwargs.get('pk')
        user_pk = self.request.user.id
        text = get_object_or_404(Text, pk=text_pk)
        user = get_object_or_404(User, pk=user_pk)

        # フォームデータを拾って付け加える
        comment = form.save(commit=False)
        comment.text_id = text
        comment.user_id = user
        comment.save()

        return redirect('study:text_detail', pk=text_pk)

class ThreadCreate(CreateView):
    "教材へのスレッド作成、ページは表示されず、作成のために必要"
    form_class = ThreadForm
    model = Thread

    def form_valid(self, form):
        "フォームが送信された後に、スレッドの紐づく教材、ユーザーのidをそれぞれ規定、送信後は教材画面を表示"
        # 登録オブジェクトの取得
        text_pk = self.kwargs.get('pk')
        user_pk = self.request.user.id
        text = get_object_or_404(Text, pk=text_pk)
        user = get_object_or_404(User, pk=user_pk)

        # フォームデータを拾って付け加える
        comment = form.save(commit=False)
        comment.text_id = text
        comment.user_id = user
        comment.save()

        return redirect('study:text_detail', pk=text_pk)

class ThreadDetail(LoginRequiredMixin,DetailView):
    "スレッドの詳細ページ"
    template_name = 'study/thread_detail.html'
    model = Thread

    # スレッド詳細ページにおいてスレッドの返信もできるための処理
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # テンプレートにコメント作成フォーム、スレッド作成フォームを渡す
        context['reply_form'] = ReplyForm

        return context

class ReplyCreate(CreateView):
    "スレッドへの返信作成、ページは表示されず、作成のために必要"
    model = Reply
    form_class = ReplyForm

    def form_valid(self, form):
        "フォームが送信された後に、スレッドの紐づく教材、ユーザーのidをそれぞれ規定、送信後は教材画面を表示"
        # 登録オブジェクトの取得
        thread_pk = self.kwargs.get('pk')
        user_pk = self.request.user.id
        thread = get_object_or_404(Thread, pk=thread_pk)
        user = get_object_or_404(User, pk=user_pk)

        # フォームデータを拾って付け加える
        comment = form.save(commit=False)
        comment.thread_id = thread
        comment.user_id = user
        comment.save()

        return redirect('study:thread_detail', pk=thread_pk)

class Analysis(TemplateView):
    "自己分析ツール一覧ページ"
    template_name = 'study/analysis.html'

class Enneagram(TemplateView):
    "エニアグラム診断ページ"
    template_name = 'study/enneagram.html'

    def get_context_data(self, **kwargs):
        "アンケートを作るための準備"
        context = super().get_context_data(**kwargs)
        # エニアグラムの質問と対応するタイプのリスト取得
        enneagram_data = read_csv('enneagram_question.csv')
        # 質問だけにする
        questions = []
        for lis in enneagram_data:
            questions.append(lis[0])

        context['questions'] = questions

        return context

    def post(self, request, *args, **kwargs):
        "回答結果をもとに結果画面表示を準備"
        # エニアグラムの質問と対応するタイプのリスト取得
        enneagram_data = read_csv('enneagram_question.csv')
        enneagram_topic = read_csv('enneagram_topic.csv')
        # 得られた回答の情報をまとめる
        ans_data = []
        for i in range(len(enneagram_data)):
            ans_data.append(request.POST[str(i+1)])
        # 得られた回答から結果を集計
        result_data = [0,0,0,0,0,0,0,0,0]
        for i,data in enumerate(ans_data):
            result_data[int(enneagram_data[i][1])-1] += int(data)

        context = super().get_context_data(**kwargs)
        for i,data in enumerate(result_data):
            data *= 4/3
            data = round(data)
            result_data[i] = data

        result_type = 0
        result_type_data = 0

        # その人のタイプを把握する、全て同じ度合いの時タイプ1とする
        for i,data in enumerate(result_data):
            if data > result_type_data:
                result_type_data = data
                result_type = i

        topic = []
        # topicのindex0~5にそのタイプの性質、6にそのタイプ番号を格納
        for i in range(7):
            topic.append(enneagram_topic[result_type][i])
        topic.append(result_type)

        context['result_data'] = result_data
        context['topic'] = topic

        return render(request,'study/enneagram_result.html',context)

class EnneagramResult(TemplateView):
    "エニアグラム診断結果ページ"
    template_name = 'study/enneagram_result.html'
