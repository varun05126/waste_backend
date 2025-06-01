# urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from core import views

urlpatterns = [
    # IMPORTANT: Place your specific admin-prefixed URLs BEFORE the general 'admin/' path
    path('admin/pickups/', views.list_pickup_requests, name='list_pickup_requests'),

    path('admin/', admin.site.urls),  # This should come AFTER your specific admin-prefixed URLs

    path('', views.homepage, name='homepage'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('pickup/', views.pickup, name='pickup'),
    path('reqs/', views.reqs, name='reqs'),
    path('api/chatbot/', views.chatbot_response, name='chatbot_response')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)