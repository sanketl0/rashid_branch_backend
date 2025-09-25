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
from django.urls import include, path
from .import views 
from rest_framework import routers
from coa.views import  coaList,  coaViewSet, COATransactionsGenericAPIView, accountheadViewSet, accountheadList,  openingbalanceViewSet,  openingbalanceList, COAGenericAPIView
from .views import *
router = routers.SimpleRouter()
#Add Coa Api Is Here addmultiplecoaopeningbalance
router.register('addcoa', coaViewSet)
#Add coa Account head creating Api Means New coa head created and uder the type will be created
router.register('addaccounthead', accountheadViewSet)
#Chart of account Opening balance  Apigetcoaob
router.register('addopeningbalance', openingbalanceViewSet)
#Multiple Char of Account Opening Balance Coa 
# router.register('addmultiplecoaopeningbalance', Opening_BalanceViewSet, basename='addmultiplecoaopeningbalance')

urlpatterns = [
    path('', include(router.urls)),
    path('addcoa/', coaList.as_view()), #post url for coa
    path('addTax/', TaxView.as_view()),
    path('getGst/<uuid:company_id>/<str:name>/',TaxView.as_view()),
    path('addCoaSubhead/',CoaSubheadView.as_view()),
    path('updateCoa/<uuid:pk>/', CoaSubheadView.as_view()),
    path('getCoaSubHead/<uuid:comp_id>/',CoaSubheadView.as_view()),
    path('getCoaSubHeadByAccountName/<uuid:comp_id>/<str:acc_name>/',CoaSubheadSearchView.as_view()),
    path('getCoaSubHeadByAccountType/<uuid:comp_id>/<str:acc_type>/',CoaSubheadSearchView.as_view()),
    path('getCoaSubHeadByAccountType/<uuid:comp_id>/<str:acc_type>/',CoaSubheadSearchView.as_view()),
    path('getCoaWholeData/<uuid:comp_id>/',CoaWholeView.as_view()),
    path('getcoa', coaList.as_view()), #get url coa 
    #get the Coa By Company Id Coa Will be Created base Featch Data in 
    #company creation Time and company creted and then company id added in getCOADetailsByaccount_nameCoa table
    path('getcoashortpaginationbycompanyid/<uuid:comp_id>/',views.getcoashortpaginationbycompanyid,name='CoaCompany'),
    path('getcoashortbycompanyid/<uuid:comp_id>/',views.getcoashortbycompanyid),
    #Featch the Account name in Coa Table in account name wise
    path('getcoabyaccountname/', views.accountname, name='account'),
    #featch the data company id wise account name
    path('getcoabyaccountnamecompanyid/<uuid:comp_id>/', views.accountnameshortbycompanyid, name='account'),
    path('getallcoas/<uuid:comp_id>/',views.accountnamesdefaulthortbycompanyid),
    #path('getcoatransactionsbyid/<uuid:pk>', COATransactionsGenericAPIView.as_view()), #get all transactionwise chart of account by coa_id
    
    #Get the data Journal Transaction data in Coa id wise
    path('getcoatransactionsbyid/<uuid:from_to_id>',views.getJRNLTransbyCOAID,name='CoaMast Transaction'),
    path('getcoatransactionsbycoa_id/<uuid:from_to_id>',views.getJRNLTransbyCoaId,name='CoaMast Transaction'),
    path('getcoatransactionsby_id/<uuid:from_to_id>',views.getJRNLTransbyId,name='CoaMast Transaction'),
    #path('getCOA', views.coaCreation, name='coa'),
    
    #Geting the Chart of Account in coa id wise return in coa table 
    path('getcoabyid/<uuid:pk>/', views.coaDetail, name='getcoabyid'),
    #update Coa Api
    path('updatebyid/<uuid:pk>/', views.coaUpdate, name='updatebyid'),

    #Account Head
    path('addaccounthead/', accountheadList.as_view()), #post url   
    path('getaccounthead', accountheadList.as_view()), #get url
    #path('getAccountHead', views.accountheadCreation, name='accounthead'),
    #Account Head id wise
    path('getaccountheadbyid/<uuid:pk>/', views.AccountHeadDetail, name='getaccountheadbyid'),
    #Account Head Id Wise
    path('updatebyid/<uuid:pk>/', views.AccountHeadUpdate, name='updatebyid'),

    #Opening Balance
    # path('addopeningbalance/', openingbalanceList.as_view()), #post url   
    path('getopeningbalance', openingbalanceList.as_view()), #get url
    path('getcoaob/<uuid:comp_id>/', views.obshortbycompanyid,name='opening_balance'),
    #path('getopeningbalance', views.openingbalanceCreation, name='openingbalance'),
    #path('getallopeningbalance/', views.OpeningBalanceRightJoin, name='getallopeningbalance'),
    
    #geting the opening  balance in id through 
    path('getopeningbalancebyid/<uuid:pk>/', views.OpeningBalanceDetail, name='getopeningbalancebyid'), 
    #updating the coa in the coa id wise
    path('updatecoaobbyid/<uuid:pk>/', views.coaobUpdate, name='updatecoaobbyid'),
    #this Api is used to updating the customer opening balance in id wise
    path('updatecustomerobbyid/<uuid:pk>/', views.customerobUpdate, name='updatecustomerobbyid'),
    
    path('getCOADetailsByaccount_name/<uuid:company_id>/<str:name>/',views.getCOADetailsByaccount_name),
    path('getCOADetailsByaccount_type/<uuid:company_id>/<str:account_type>/',views.getCOADetailsByaccount_type),
    path('getAsyncCoaType/<uuid:comp_id>/<str:name>/<str:account_type>/',CoaAsyncWholeView.as_view()),
    path('getAsyncCoa/<uuid:comp_id>/<str:name>/<str:account_subhead>/',CoaAsyncWholeView.as_view()),
    path('getAsyncIncomeCoa/<uuid:comp_id>/<str:name>/<str:income>/', CoaAsyncWholeView.as_view()),
    path('getAsyncCoa/<uuid:comp_id>/<str:name>/', CoaAsyncWholeView.as_view()),
    path('getAsyncCoaAssLiab/<uuid:comp_id>/<str:name>/', CoaAsyncAssetLiabView.as_view()),

]


