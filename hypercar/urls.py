"""hypercar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from tickets.views import WelcomeView, MenuView, OperationView, ProcessingView
from django.views.generic import RedirectView

urlpatterns = [
    path('welcome/', WelcomeView.as_view()),
    path('menu/', MenuView.as_view()),
    re_path('get_ticket/(?P<operation>\w+)', OperationView.as_view()),
    path('processing', ProcessingView.as_view()),
    path('processing/', RedirectView.as_view(url='/processing'))
]
# \d+ means one or more digit [0-9] (depending on LOCALE)
# \d- means a digit followed by a dash -

# \w+ means one or more word character [a-zA-Z0-9_] (depending on LOCALE)
# \w- means a word char followed by a dash -
