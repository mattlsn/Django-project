from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login

User = get_user_model()

# Create your views here.


@require_http_methods(["GET", 'POST'])
def Mylogin(request):
    if request.method == 'GET':
        return render(request, template_name='login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                form.add_error(field='email', error="信箱或密碼錯誤")
                return render(request, template_name='login.html', context={'form':form})


@require_http_methods(["GET", 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, template_name='register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('Mattauth:login'))
        else:
            print(form.errors)
            return render(request, template_name='register.html', context={'forms':form})


def send_email_captcha(request):
    # ?email=xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message":"必需輸入郵件"})
    # 生成驗證碼
    captcha = "".join(random.sample(string.digits, k=4))
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha':captcha})
    send_mail(subject="Matt部落格郵件認證", message=f'你的驗證碼是{captcha}', recipient_list=[email],from_email=None)
    return JsonResponse({"code":200, "message":'郵件發送成功'})
