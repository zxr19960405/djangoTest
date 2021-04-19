from django.db import models

# Create your models here.


class Rank(models.Model):
    """
    分数排名
    """
    client = models.CharField(max_length=100, db_index=True, verbose_name='客户端名称')
    score = models.IntegerField(db_index=True, verbose_name='分数')

    class Meta:
        verbose_name = '分数排名'
