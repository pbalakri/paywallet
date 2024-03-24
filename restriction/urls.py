from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"student/<int:student_id>",
         views.StudentRestrictionsView.as_view(), name="student_restrictions"),
    path(r"student/<int:student_id>/payment",
         views.StudentPaymentRestrictionView.as_view(), name="payment_restrictions"),
    path(r"student/<int:student_id>/category",
         views.StudentCategoryRestrictionView.as_view(), name="category_restrictions"),
    path(r"student/<int:student_id>/product",
         views.StudentProductRestrictionView.as_view(), name="product_restrictions"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
