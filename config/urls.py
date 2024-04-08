from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import HomeView, Review_listView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', Review_listView.as_view(), name='home_review'),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('books/', include('books.urls')),
    
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)