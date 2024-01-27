from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"store/<str:store_id>/products/category/<str:category_id>",
         views.GetProductsPerCategoryView.as_view(), name="get_products_category"),
    path(r"store/<str:store_id>/products/<str:product_id>",
         views.GetProduct.as_view(), name="get_product"),
    path(r"store/<str:store_id>/products/",
         views.GetProducts.as_view(), name="get_products"),
    path(r"store/<str:store_id>/categories/",
         views.GetCategories.as_view(), name="get_categories"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
