from django.urls import path
from . import views

urlpatterns = [
    path('api/game/postMessage/', views.postMessage),
    path('api/game/getFirstMessage/', views.getFirstMessage),
    path('api/game/loadModel/', views.loadModel),
]