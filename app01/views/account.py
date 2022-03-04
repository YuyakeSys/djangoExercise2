from django.shortcuts import render, HttpResponse, redirect
from django import forms
from io import BytesIO

from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.code import check_code
from app01.utils.encrypt import md5


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="username",
        widget=forms.TextInput,
        required=True,
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(render_value=True),
        required=True,
    )
    code = forms.CharField(
        label="authentication code",
        widget=forms.PasswordInput(render_value=True),
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("username", "wrong username or password")
            return render(request, 'login.html', {"form": form})
        # session
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        request.session.set_expiry(60 * 60 * 24 * 5)
        return redirect('/admin/list/')

    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.clear()

    return redirect('/login/')


def image_code(request):
    """图形验证码"""
    img, code_string = check_code()

    request.session['image_code'] = code_string
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
