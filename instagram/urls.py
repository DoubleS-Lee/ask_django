from django.urls import path, re_path, register_converter   # path를 사용하기 위해 import
from . import views # post_list 함수를 사용하기 위해 views 파일을 import 한다
from .converters import YearConverter, MonthConverter, DayConverter

register_converter(YearConverter, 'year')
register_converter(MonthConverter, 'month')
register_converter(DayConverter, 'day')

app_name = 'instagram'

urlpatterns =[
    path('', views.post_list, name='post_list'),   # 함수를 호출하는게 아니어서 views.post_list() 가 아니고 그냥 함수 그 자체를 넘기기 때문에 다음과 같이 써줌
    path('<int:pk>/', views.post_detail, name='post_detail'),
    # re_path(r'(?P<pk>\d+)/$', views.post_detail),

    # path('archives/<year:year>/', views.archives_year),
    # path('archives/<int:year>/', views.archives_year),
    # re_path(r'archives/(?P<year>20\d{2})/', views.archives_year),

    path('archive/', views.post_archive, name='post_archive'),
    path('archive/<year:year>/', views.post_archive_year, name='post_archive_year'),
    # path('archive/<year:year>/<month:month>/', views.post_archive_month, name='post_archive_month'),
    # path('archive/<year:year>/<month:month>/<day:day>/', views.post_archive_day, name='post_archive_day'),

    path('new/', views.post_new, name='post_new'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),

]