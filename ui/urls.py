from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^',
        login_required(TemplateView.as_view(template_name='index.html')),
        name='home')]
