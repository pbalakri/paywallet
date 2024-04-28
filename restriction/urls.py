from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"student/<str:registration_number>",
         views.StudentRestrictionsView.as_view(), name="student_restrictions"),
    path(r"student/<str:registration_number>/payment",
         views.StudentPaymentRestrictionView.as_view(), name="payment_restrictions"),
    path(r"student/<str:registration_number>/category",
         views.StudentCategoryRestrictionView.as_view(), name="category_restrictions"),
    path(r"student/<str:registration_number>/product",
         views.StudentProductRestrictionView.as_view(), name="product_restrictions"),
    path(r"", views.AllergiesView.as_view(), name="allergies"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
