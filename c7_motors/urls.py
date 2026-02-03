#URL configuration for c7_motors project.

from django.urls import path , include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView 
from c7_app.admin import custom_admin_site 
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from c7_app.sitemap import (HomeSitemap,InventorySitemap,CarDetailSitemap,StaticViewSitemap,ArticlesSitemap,)

sitemaps = {
    'home': HomeSitemap,
    'inventory': InventorySitemap,
    'cars': CarDetailSitemap,
    'static': StaticViewSitemap,
    'articles': ArticlesSitemap,
}

urlpatterns = [
    path('admin/', custom_admin_site.urls),

    path(
        "sitemap.xml",
        cache_page(60 * 60 * 6)(sitemap),
        {"sitemaps": sitemaps},
        name="sitemap",
    ),

    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"
        ),
    ),

    path('i18n/', include('django.conf.urls.i18n')),

    path('', include('c7_app.urls')),
]

custom_admin_site.index_title = "C7 Motors"
custom_admin_site.site_header = "C7 Motors Administration"

urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
