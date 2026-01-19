from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    path('', views.TourListView.as_view(), name='index'),
    path('tour/<slug:slug>/', views.TourDetailView.as_view(), name='detail'),
    path('tour/<slug:slug>/order/', views.OrderCreateView.as_view(), name='order'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('offline/', views.offline, name='offline'),
]
