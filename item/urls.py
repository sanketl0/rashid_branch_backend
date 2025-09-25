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
    1. Import the include() function: from django.urls import include, pathgetitemstockreport
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from item.viewsets import *
from .views import *
from item.viewsets.stock_transfer_view import *
from item.viewsets.manufacture_view import *
router = routers.SimpleRouter()
# Cretaing the Item 
router.register('additem', itemViewSet)
#Creating the manual adjustment 
#Inventory Item It can adjust means item stock item ,item rate etc
router.register('addajustment', AdjustmentViewSet)



urlpatterns = [
    path('addItemGroup/',ItemGroupView.as_view()),
    path('addGodown/',GodownView.as_view()),
    path('getGodownByName/<str:name>/<uuid:branch_id>/',GodownView.as_view()),
    path('updateItemGroup/<uuid:pk>/',ItemGroupView.as_view()),
    path('', include(router.urls)),
    path('test-item/<uuid:item_id>/,',TestUpdateView.as_view(),name='update_item'),
    path('addStockTransfer/',StockTransferView.as_view()),
    path('addMfg/', ManufactureView.as_view()),
    path('addStockJournal/', StockJournalView.as_view()),
    path('getmfgById/<uuid:pk>/', ManufactureView.as_view()),
    path('getstkById/<uuid:pk>/', StockJournalView.as_view()),
    path('updateMfg/<uuid:pk>/', ManufactureView.as_view()),
    path('updateStockJournal/<uuid:pk>/', StockJournalView.as_view()),
    path('getmfgshortAllbycompanyid/<uuid:company_id>/<uuid:branch_id>/', ManufactureView.as_view()),
    path('getstkshortAllbycompanyid/<uuid:company_id>/<uuid:branch_id>/', StockJournalView.as_view()),
    path('edit-item/<uuid:pk>/', ItemUpdateView.as_view()),
    # get the all item in item tabel
    path('getitem', itemList.as_view()),
    #path('getitem', views.itemCreation, name='item'),
    #path('getitemshort', views.ShortItemDetails, name='item'),
    path('getitemshortbycompanyid/<uuid:comp_id>/', getitemshortbycompanyid, name='item'),
    path('getitemshortAllbycompanyid/<uuid:comp_id>/<uuid:branch_id>/',ShortItemAll),

    path('getitemshortAllbyName/<uuid:comp_id>/<uuid:branch_id>/<str:name>/', ShortAsyncItemAll),
    path('getFullItemShortAllbyName/<uuid:comp_id>/<uuid:branch_id>/<str:name>/', ShortAsyncFullItemAll),
    #get the item short by company id wise
    path('getitemshortpaginationbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', getitemshortpaginationbycompanyid, name='item'),
    path('getstocktransfershortpaginationbycompanyid/<uuid:comp_id>/<uuid:branch_id>/', StockTransferView.as_view(), name='item'),
    path('getstocktransferbyid/<uuid:pk>/', StockTransferView.as_view(), name='item'),
    path('getStock/<uuid:pk>/<uuid:branch_id>/', getBatchStockView),
    # get the item in item id wise
    path('getitembyid/<uuid:pk>/', itemDetail, name='getitembyid'),
    #updating the a item by id wise
    path('UpdateById/<uuid:pk>/', itemUpdate, name='UpdateById'),
    #this is the basic inventory managemnt methods to check and exolre the methods
    #Inventory item report in first item in firts out to check the item and stock tables
    path('getfifostockdetailsbyitemid/<uuid:item_id>/', getFIFOstock_details, name='FIFOStock_Details'),
    #Inventort item report in Last in first out check the item and stock tables 
    path('getlifostockdetailsbyitemid/<uuid:item_id>/', getLIFOstock_details, name='LIFOStock_Details'),
    #Weightd Avarage cost api its inventory methos in inventory section
    path('getwacstockdetailsbyitemid/<uuid:item_id>/', getWACstock_details, name='WACStock_Details'),
    #item stock report to chekc stock in and stock out
    path('getitemstockreport/<from_date>/<to_date>/<uuid:comp_id>/<uuid:branch_id>/', getitemstockreport, name='getitemstockreport'),
    #geting the only item stock amount value
    path('getitemamountvalue/<uuid:item_id>/<uuid:branch_id>/', getstockitemamountvalue, name='getstockitemamountvalue'),
    path('getItemTransaction/<uuid:item_id>/',getitemtransaction),
    #addjustment short by company id wise
    path('addjustmentshortbycompanyid/<uuid:company_id>/<uuid:branch_id>/', adjustmentshortbycompanyid, name='adjustmentshortbycompanyid'),
    #Stock adjustment full view 
    path('fullviewadj/<uuid:adj_id>/',addjustmentfullview, name='addjustmentfullview'),
    #Inventory valutiion 
    path('getstockiteminventoyvalution/<uuid:item_id>/', getstockiteminventoyvalution, name='getstockiteminventoyvalution'),
    path('getItemDetailsByItemName/<uuid:company_id>/<uuid:branch_id>/', getItemDetailsByItemName, name='getItemDetailsByItemName'),
    path('getItemDetailsByItemCatagory/<uuid:company_id>/<uuid:branch_id>/', getItemDetailsByItemCatagory, name='getItemDetailsByItemCatagory'),
    path('getAdjustmentDetailsByItemName/<uuid:company_id>/<str:name>/', getAdjustmentDetailsByItemName, name='getAdjustmentDetailsByItemName'),
    path('getAdjustmentDetailsBystatus/<str:track_inventory>/', getAdjustmentDetailsBystatus, name='getAdjustmentDetailsBystatus'),
    path('getAdjustmentDetailsByReference/<uuid:company_id>/<uuid:branch_id>/<str:reference>/', getAdjustmentDetailsByReference),
    path('getManufactureByName/<uuid:branch_id>/', getManufactureByName),
    path('getManufactureByReference/<uuid:branch_id>/', getManufactureBySerial),

]
