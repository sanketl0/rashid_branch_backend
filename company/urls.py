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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path, re_path
from .import views
from rest_framework import routers
from company.views import  *
from coa.views import Opening_BalanceViewSet
router = routers.SimpleRouter()
#This Api Is Used to create the Company means Post the Company
router.register('addcompany', companyViewSet)
#This APi Is Can't Use its api is creating the Branch

#This Api Is used to Update the Company in Existing Our Company Model
router.register('companyupdate', CompanyUpdateViewset)
router.register('addmultiplecoaopeningbalance', Opening_BalanceViewSet, basename='addmultiplecoaopeningbalance')
urlpatterns = [
    #Company    
    path('', include(router.urls)),
    path('addBranch/',branchViewSet.as_view()),
    path('updateBranch/<uuid:pk>/',branchViewSet.as_view(),name='update-branch'),
    # Api Is Used Comapy All data Returncompanyupdate
    #Both are same working but ui dependancy so cannot be deleted
    path('company/', companyList.as_view()),    
    path('getcompany', companyList.as_view()),
    # This Api is All Company name is return
    path('getallcompanyname/', views.AllCompanyNameDetails, name='getallcompanyname'),
    # Short By Company Id 
    path('getcompanybyid/<uuid:pk>/', views.companyDetail, name='getcompanybyid'),
    #Updated Api Function base
    path('updatebyid/<uuid:pk>/', views.companyUpdate, name='updatebyid'),
    path('getallcompanydetails/', views.GetAllCompanyDetails, name='GetAllCompanyDetails'),
    #Branch
    # All Api Is Branach APi Only Creating the backend Side
    # UI And Client Side Functinality Not Working 
    #In Feature Brance section excuted to Same As well company 
    path('branch/', branchList.as_view()),
    path('getbranch/<uuid:comp_id>', branchList.as_view()),
    path('getbranchbyid/<uuid:pk>/', views.branchDetail, name='getbranchbyid'),   
    path('getbranchshort', views.ShortBranchDetails, name='branch'),   
    path('groupbycompanyname/<uuid:comp_id>/', group_by_company,name='groupbycompanyname') ,
    path('getCompanyDetailsByCompanyName/<str:company_name>/',getCompanyDetailsByCompanyrName),
    path('getCompanyDetailsByCompanyType/<str:company_type>/',getCompanyDetailsByCompanyType),
    path('getFeatures/',planFeatureView),
    path('getDefaults/<uuid:comp_id>/<uuid:branch_id>/', DefautlView.as_view()),
    path('updateDefault/<uuid:comp_id>/<uuid:branch_id>/', DefautlView.as_view()),


    
]
