from django.urls import path
from ocr.views import *
urlpatterns = [
    path('upload/',DocumentView.as_view()),
    path('get-uploads/<uuid:comp_id>/<uuid:branch_id>/',DocumentView.as_view()),
    path('get-result/<uuid:doc_id>/<str:doc_type>/',ResultView.as_view()),
    path('put-result/<uuid:doc_id>/', ResultView.as_view()),
    path('get-uploads-name/<uuid:comp_id>/<uuid:branch_id>/<str:name>/',DocumentNameView.as_view())

]