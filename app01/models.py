from django.db import models


# Create your models here.
class Department(models.Model):
    title = models.CharField(verbose_name='title', max_length=32)


class UserInfo(models.Model):
    name = models.CharField(verbose_name="name", max_length=16)
    password = models.CharField(verbose_name="password", max_length=64)
    age = models.IntegerField(verbose_name="age")
    account = models.DecimalField(verbose_name="account", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="time")

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")
    # ### 3.1 级联删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # ### 3.2 置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="sex", choices=gender_choices)
