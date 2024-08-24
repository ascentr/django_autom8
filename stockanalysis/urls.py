from django.urls import path
from . import views

urlpatterns = [
     path('stocks/', views.stocks, name='stocks'),
     path('stock-autocomplete/', views.StockAutocomplete.as_view(), name='stock-autocomplete', ),
     path('stock-detail/<int:id>', views.stock_detail, name='stock-detail'),
]
