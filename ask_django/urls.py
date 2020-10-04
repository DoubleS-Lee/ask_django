"""ask_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

# from django.conf import global_settings
# from ask_django import settings
from django.conf import settings    #위 2개를 하나로 합쳐준 형태

urlpatterns = [
    # path('', TemplateView.as_view(template_name = 'root.html'), name='root'),
    path('', RedirectView.as_view(
        #url='/instagram/'                                  # 밑에 pattern_name과 같은 기능, 밑의 기능을 더 추천
        pattern_name='instagram:post_list'), name='root'),
    path('admin/', admin.site.urls),
    path('instagram/', include('instagram.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:  # settings.py의 DEBUG가 TRUE일 경우 실행(실제 서버에 올릴때는 False가 됨)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)  # urlpatterns에 미디어 파일에 대한 정보를 추가한다

    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
