"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.ur
    ls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from .import views
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
#router.register('addmanualjournal', manualjournalViewSet)
router.register('addmanualjournal', new1journalViewSet, basename='addmanualjournal')
router.register('addjournaltransaction', journaltransactionViewSet)
router.register('updatemanualjournal', ManualJournalupdateViewsets)
urlpatterns = [
    path('', include(router.urls)),
    path('update-journal/<uuid:pk>/',UpdateJournalView.as_view()),
    #path('getmanualjournal', manualjournalList.as_view()), 
    #path('getjournaltransaction', JournalTransactionGenericAPIView.as_view()), 
    path('getmanualjournal', JournalTransactionGenericAPIView.as_view()), 
    # path('getmanualjournalbyid/<uuid:pk>/', JournalTransactionGenericAPIView.as_view()),#get journal transaction byid   
    path('getmanualjournalbyid/<uuid:pk>/',views.getmastermanualjournalshortbymjid,name='mastjournal'),   
    path('getmanualjournalshort', views.shortmanualjournalDetails, name='mj'),
    #path('getmanualjournalbyid/<uuid:pk>/', views.manualjournalDetail, name='getmjbyid'),    
    path('updatemanualjournalbyid/<uuid:pk>/', views.manualjournalupdate, name='updatemjbyid'),
    path('getmanualjournalshortbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', views.getmanualjournalshortbycompanyid, name='manualjournal'),
    path('getMJDetailsByserial/<uuid:company_id>/<uuid:branch_id>/',views.getMJDetailsByserial),
    path('getMJDetailsByreference/<uuid:company_id>/<uuid:branch_id>/',views.getMJDetailsByreference)
]

# urlpatterns = [
#     #ManualJournal
#     path('getManualJournal', views.manualjournalCreation, name='manualjournal'),
#     path('getManualJournalById/<int:pk>/', views.manualjournalDetail, name='getManualJournalById'),
#     path('UpdateById/<int:pk>/', views.manualjournalUpdate, name='UpdateById'),

#     #RecJournal
#     path('getRecJournal', views.recjournalCreation, name='recjournal'),
#     path('getRecJournalById/<int:pk>/', views.recjournalDetail, name='getRecJournalById'),
#     path('UpdateById/<int:pk>/', views.recjournalUpdate, name='UpdateById'),

#     #BulkUpdate
#     path('getBulkUpdate', views.bulkupdateCreation, name='bulkupdate'),
#     path('getBulkUpdateById/<int:pk>/', views.bulkupdateDetail, name='getBulkUpdateById'),
#     path('UpdateById/<int:pk>/', views.bulkupdateUpdate, name='UpdateById'),

#     #Budget
#     path('getBudget', views.budgetCreation, name='budget'),
#     path('getBudgetById/<int:pk>/', views.budgetDetail, name='getBudgetById'),
#     path('UpdateById/<int:pk>/', views.budgetUpdate, name='UpdateById'),
    
# ]
