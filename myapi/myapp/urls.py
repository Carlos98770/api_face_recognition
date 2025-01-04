from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import UserViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'users', UserViewSet,basename='user')

urlpatterns = [
    #path('users/', UserViewSet.as_view({'post': 'create'}), name='user-list'),
    #path('users/<int:pk>/', UserViewSet.as_view({'get': 'update'}), name='user-detail'),
    path('api/', include(router.urls)),
    path('api/users/check/', UserViewSet.as_view({'post': 'check'}), name='user-check')

]

# Adiciona as URLs para servir os arquivos de mídia em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
