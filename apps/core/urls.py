from django.urls import path

from apps.core.views import ChoicesView

urlpatterns = [
    path('choices', ChoicesView.as_view(), name='choices'),
]
