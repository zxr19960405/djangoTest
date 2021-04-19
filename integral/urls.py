# -*- coding: utf-8 -*-
from django.urls import path
from . import views

urlpatterns = [
    path('rank', views.get_rank_list, name='get_rank_list'),
    path('update_rank', views.update_rank, name='update_rank')
]
