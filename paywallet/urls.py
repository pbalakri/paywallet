"""
URL configuration for paywallet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken import views
admin.site.site_url = ''
admin.site.site_header = _("PayWay Admin")
admin.site.site_title = _("PayWay Admin")
admin.site.index_title = _("Welcome to PayWay Admin")

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/schools/', include("school.urls")),
    path('api/wallets/<str:rfid>/', include("wallet.urls")),
    path('api/schools/<str:school_id>/store/', include("school_store.urls")),
    path('api/guardian/', include("guardian.urls")),
    path('api/restrictions/', include("restriction.urls")),
    # path('', include('admin_material.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    re_path(r'^rosetta/', include('rosetta.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    prefix_default_language=False)
