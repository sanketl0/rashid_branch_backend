from django.urls import include, path
from subuser.views import *

urlpatterns = [
    path('create-subuser/', SubUserView.as_view()),
    path('get-subuser/', SubUserView.as_view()),
    path('get-subuser/<int:pk>', SubUserView.as_view()),
    path('update-subuser/<int:pk>/', SubUserView.as_view()),
]