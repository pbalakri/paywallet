from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"products",
         views.GetMerchantProducts.as_view(), name="get_merchant_products"),
    #     path(r"orders",
    #          views.Createorder.as_view(), name="create_merchant_order"),


]
urlpatterns = format_suffix_patterns(urlpatterns)
