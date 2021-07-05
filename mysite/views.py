import os
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from blog.models import Article
from mysite.forms import UserCreationForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.mail import send_mail


def index(request):
    ranks = Article.objects.order_by('-count')[:2]
    objects = Article.objects.all()[:3]
    context = {
        'articles': objects,
        "ranks": ranks
    }
    return render(request, 'mysite/index.html', context)


class Login(LoginView):
    template_name = 'mysite/auth.html'

    def form_valid(self, form):
        messages.success(self.request, 'ログインに成功しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'ログインに失敗しました')
        return super().form_invalid(form)


def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_active = False # メールアドレスの検証などをするときは一度Falseにして、検証が完了したらTrueに戻す
            user.save()
            login(request, user)
            messages.success(request, '登録に成功しました。')
            return redirect('/')
    return render(request, 'mysite/auth.html', context)


@login_required
def mypage(request):
    user = request.user
    context = {
        "user": user
    }
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, '更新に成功しました。')
    return render(request, 'mysite/mypage.html', context)


def contact(request):
    context = {
        'grecaptcha_siteky': os.environ['GRECAPTCHA_SITEKEY']
    }
    if request.method == 'POST':
        recaptcha_token = request.POST.get('g-recaptcha-response')
        res = grecaptcha_request(recaptcha_token)
        if not res:
            messages.success(request, '人間の認証に失敗しました。')
            return render(request, 'mysite/contact.html', context)
        # --- notify me
        subject = 'お問い合わせがありました。'
        message = """お問い合わせがありました\n\n名前：{}\nメールアドレス：{}\n内容：{}""".format(
            request.POST.get('name'),
            request.POST.get('email'),
            request.POST.get('content')
        )
        email_from = os.environ['DEFAULT_EMAIL_FROM']
        email_to = [os.environ['DEFAULT_EMAIL_FROM']]
        send_mail(subject, message, email_from, email_to)
        messages.success(request, 'お問い合わせいただきありがとうございます。')
        # --- notify me
    return render(request, 'mysite/contact.html', context)


def grecaptcha_request(token):
    from urllib import request, parse
    import json
    import ssl

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    url = "https://www.google.com/recaptcha/api/siteverify"
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'secret': os.environ['GRECAPTCHA_SECRETKEY'],
        'response': token
    }
    data = parse.urlencode(data).encode()
    req = request.Request(url, method="POST", headers=headers, data=data)
    f = request.urlopen(req, context=context)
    response = json.loads(f.read())
    f.close()
    print('---response---')
    print(response)
    print('---response---')
    return response['success']
