from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/',    views.login_view,    name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/',   views.logout_view,   name='logout'),

    # App
    path('',              views.dashboard_view,  name='dashboard'),
    path('diagnostico/',  views.diagnostico_view, name='diagnostico'),
    path('api/summary/',  views.ai_summary_view, name='api_summary'),
]
