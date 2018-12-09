# -*- coding: utf-8 -*-

from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True, )
    username = models.CharField(max_length=30)
    group = models.CharField(max_length=30, null=True)
    status = models.IntegerField(null=True)

    class Meta:
        db_table = "816_user"


class Attend(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    attend_status = models.IntegerField()  # -1 请假  1 出勤  -2 缺勤
    localhost = models.CharField(max_length=100, verbose_name='地点')
    category = models.IntegerField(validators='上榜分类')  # 0没有上榜 1灭敌上榜 2 拆迁上榜 3 双榜
    task_date = models.DateTimeField(verbose_name='任务时间')

    class Meta:
        db_table = "816_attend"
