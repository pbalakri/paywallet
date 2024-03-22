from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"merchant/<str:merchant_id>/products/",
         views.GetProducts.as_view(), name="get_merchant_products"),
    path(r"merchant/<str:merchant_id>/orders/",
         views.Createorder.as_view(), name="create_merchant_order"),


]
urlpatterns = format_suffix_patterns(urlpatterns)
