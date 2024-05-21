from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"products/category/<str:category_id>",
         views.GetProductsPerCategoryView.as_view(), name="get_products_category"),
    path(r"products/<str:product_id>",
         views.GetProduct.as_view(), name="get_product"),
    path(r"products",
         views.GetProducts.as_view(), name="get_products"),
    path(r"categories",
         views.GetCategories.as_view(), name="get_categories"),
    path(r"orders/",
         views.GetOrders.as_view(), name="get_orders"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
