from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
# Create your views here.
from app01 import models


def depart_list(request):
    """ 部门列表 """

    # 去数据库中获取所有的部门列表
    #  [对象,对象,对象]
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, 'depart_add.html')

    # 获取用户POST提交过来的数据（title输入为空）
    title = request.POST.get("title")

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回部门列表
    return redirect("/depart/list/")


def depart_delete(request):
    """ 删除部门 """
    # 获取ID http://127.0.0.1:8000/depart/delete/?nid=1
    nid = request.GET.get('nid')

    # 删除
    models.Department.objects.filter(id=nid).delete()

    # 重定向回部门列表
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """ 修改部门 """
    if request.method == "GET":
        # 根据nid，获取他的数据 [obj,]
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_object": row_object})

    # 获取用户提交的标题
    title = request.POST.get("title")

    # 根据ID找到数据库中的数据并进行更新
    # models.Department.objects.filter(id=nid).update(title=title,其他=123)
    models.Department.objects.filter(id=nid).update(title=title)

    # 重定向回部门列表
    return redirect("/depart/list/")


def user_list(request):
    """ 用户管理 """

    # 获取所有用户列表 [obj,obj,obj]
    queryset = models.UserInfo.objects.all()
    """
    # 用Python的语法获取数据
    for obj in queryset:
        print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"), obj.gender, obj.get_gender_display(), obj.depart_id, obj.depart.title)
        # print(obj.name, obj.depart_id)
        # obj.depart_id  # 获取数据库中存储的那个字段值
        # obj.depart.title  # 根据id自动去关联的表中获取哪一行数据depart对象。
    """
    return render(request, 'user_list.html', {"queryset": queryset})


def user_add(request):
    """ 添加用户（原始方式） """

    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    # 获取用户提交的数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 添加到数据库中
    models.UserInfo.objects.create(name=user, password=pwd, age=age,
                                   account=account, create_time=ctime,
                                   gender=gender, depart_id=depart_id)

    # 返回到用户列表页面
    return redirect("/user/list/")


from django import forms


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            # if name == "password":
            #     continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    """ 添加用户（ModelForm版本）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户POST提交数据，数据校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # {'name': '123', 'password': '123', 'age': 11, 'account': Decimal('0'), 'create_time': datetime.datetime(2011, 11, 11, 0, 0, tzinfo=<UTC>), 'gender': 1, 'depart': <Department: IT运维部门>}
        # print(form.cleaned_data)
        # models.UserInfo.objects.create(..)
        form.save()
        return redirect('/user/list/')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_model_form_add.html', {"form": form})


def number_list(request):
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict["mobile__contains"] = search_data
    count = models.PrettyNum.objects.filter(**data_dict).order_by("-level").count()
    total_count, div = divmod(count, 4)
    if div:
        total_count += 1
    plus = 5
    page = int(request.GET.get('page', 1))
    if total_count <= 2 * plus + 1:
        start_page = 1
        end_page = total_count
    else:
        if page <= plus:
            start_page = 1
            end_page = page*2 + 1
        else:
            if (page + plus) > total_count:
                start_page = total_count - 2 * plus
                end_page = total_count
            else:
                start_page = page - plus
                end_page = page + plus

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")[(page-1)*4+1:(page-1)*4+5]

    # 页码
    page_str = []

    # 上一页
    if page >= 1:
        prev = '<li class="page-item"><a class="page-link" href="?page={}"  aria-label="Previous"><span ' \
               'aria-hidden="true">&laquo;</span></a></li>'.format(page - 1)
    else:
        prev = '<li class="page-item"><a class="page-link" href="?page=1"  aria-label="Previous"><span ' \
               'aria-hidden="true">&laquo;</span></a></li>'
    page_str.append(prev)


    for i in range(start_page, end_page + 1):
        if i == page:
            pagi = '<li class="page-item active"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
        else:
            pagi = '<li class="page-item"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
        page_str.append(pagi)

    # 下一页
    if page < total_count:
        next_page = '<li class="page-item"><a class="page-link" href="?page={}" aria-label="Next"><span ' \
                    'aria-hidden="true">&raquo;</span></a></li>'.format(page + 1)
    else:
        next_page = '<li class="page-item"><a class="page-link" href="?page={}" aria-label="Next"><span ' \
                    'aria-hidden="true">&raquo;</span></a></li>'.format(total_count)
    page_str.append(next_page)

    page_str_list = mark_safe("".join(page_str))

    return render(request, 'pretty_list.html',
                  {"queryset": queryset, "search_data": search_data, "page_string": page_str_list})



class NumberModelForm(forms.ModelForm):
    mobile = forms.CharField(
        label="mobile number",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', 'wrong form')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            # if name == "password":
            #     continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def num_add(request):
    if request.method == 'GET':
        form = NumberModelForm()
        return render(request, 'pretty_add.html', {'form': form})
    form = NumberModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/num/list/')
    return render(request, 'pretty_add.html', {'form': form})


class NumberEditModelForm(forms.ModelForm):
    # mobile = forms.CharField(
    #     disabled=True
    # )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            # if name == "password":
            #     continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("PhoneNumberAlreadyExists")

        return txt_mobile


def num_edit(req, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if req.method == 'GET':
        form = NumberEditModelForm(instance=row_object)
        return render(req, 'pretty_edit.html', {"form": form})

    form = NumberEditModelForm(data=req.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/num/list')

    return render(req, 'pretty_edit.html', {"form": form})
