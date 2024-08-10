from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from ninja import Router

from .org.routes import auth
from .base.security import UserAuth
from .ninja_api import ninja
from .org.routes import group, org, user


# ninja routers
api_router = Router(auth=UserAuth())

# org.routes
api_router.add_router('/auth', auth.router)
api_router.add_router('/group', group.router)
api_router.add_router('/user', user.router)
api_router.add_router('/org', org.router)

# add routers to ninja
ninja.add_router('/api', api_router)

# django urls #

urlpatterns = [
    # api
    path('', ninja.urls),

    # admin
    path('admin/', admin.site.urls),
]

# media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
