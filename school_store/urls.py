from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"school/<str:school_id>/products/category/<str:category_id>",
         views.GetProductsPerCategoryView.as_view(), name="get_products_category"),
    path(r"school/<str:school_id>/products/<str:product_id>",
         views.GetProduct.as_view(), name="get_product"),
    path(r"school/<str:school_id>/products/",
         views.GetProducts.as_view(), name="get_products"),
    path(r"school/<str:school_id>/categories/",
         views.GetCategories.as_view(), name="get_categories"),
    path(r"school/orders/",
         views.GetOrders.as_view(), name="get_orders"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
