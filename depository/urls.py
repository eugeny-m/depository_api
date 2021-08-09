from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from users import urls as users_urls


class DefaultRouter(routers.DefaultRouter):
    """
    Extends `DefaultRouter` class
    to add a method for extending
    url routes from another router.
    """
    def extend(self, router):
        """
        Extend the routes with url routes of the passed in router.

        Args:
             router: SimpleRouter instance containing route definitions.
        """
        self.registry.extend(router.registry)


router = DefaultRouter()
router.extend(users_urls.router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(users_urls)),
]
