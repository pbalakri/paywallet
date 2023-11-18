from .product import Product
from django.contrib import admin
from django.db.models import Count
import random
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.filters import FieldListFilter, SimpleListFilter


class Dashboard(Product):
    class Meta:
        proxy = True
        verbose_name = _('Dashboard')
        verbose_name_plural = _('Dashboard')


class CustomCategoryListFilter(SimpleListFilter):
    title = _('category')
    parameter_name = 'category__name'

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request)
        return [(value, value) for value in queryset.values_list('category__name', flat=True).distinct()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__name=self.value())
        return queryset


class CustomRestrictionListFilter(SimpleListFilter):
    title = _('restriction')
    parameter_name = 'restriction__name'

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request)
        return [(value, value) for value in queryset.values_list('restriction__name', flat=True).distinct()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(restriction__name=self.value())
        return queryset


class DashboardAdmin(admin.ModelAdmin):

    change_list_template = 'admin/product/dashboard.html'
    list_filter = [CustomCategoryListFilter, CustomRestrictionListFilter]

    def getRandomColor(self):
        letters = list('0123456789ABCDEF')
        color = '#'
        for i in range(6):
            f = random.randint(0, 15)
            color += letters[f]
        return color

    def get_product_count_by_category(self, qs):
        labels = []
        data = []
        background_color = []
        product_count_by_category = list(qs.values('category__name').annotate(
            total=Count('category__name')))
        for i in product_count_by_category:
            labels.append(i['category__name'])
            data.append(i['total'])
            background_color.append(self.getRandomColor())
        return {
            'labels': labels,
            'datasets': [{'data': data,
                         'backgroundColor': background_color}]
        }

    def get_product_count_by_restriction(self, qs):
        labels = []
        data = []
        background_color = []
        product_count_by_restriction = list(qs.values('restriction__name').annotate(
            total=Count('restriction__name')))
        for i in product_count_by_restriction:
            labels.append(i['restriction__name'])
            data.append(i['total'])
            background_color.append(self.getRandomColor())
        return {
            'labels': labels,
            'datasets': [{'data': data,
                         'backgroundColor': background_color}]
        }

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
            response.context_data['product_count_by_category'] = self.get_product_count_by_category(
                qs)
            response.context_data['product_count_by_restriction'] = self.get_product_count_by_restriction(
                qs)
        except (AttributeError, KeyError):
            return response
        return response
