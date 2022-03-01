from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=3, label="name")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]


class NumberModelForm(BootStrapModelForm):
    mobile = forms.CharField(
        label="mobile number",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', 'wrong form')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']


class NumberEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(
    #     disabled=True
    # )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("PhoneNumberAlreadyExists")

        return txt_mobile


class NumberModelForm(BootStrapModelForm):
    mobile = forms.CharField(
        label="mobile number",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', 'wrong form')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']