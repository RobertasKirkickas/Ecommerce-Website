from django.urls import path
from . import views
from .views import (

    checkout,

    add_to_cart,
    remove_from_cart,
    OrderSummaryView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success_view, name='contact-success'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('protected/', views.ProtectedView.as_view(), name='protected'),
    path('create/', views.game_create_view, name="game_create"),
    path('list/', views.game_list_view, name="game_list"),
    path('update/<int:game_id>/', views.game_update_view, name="game_update"),
    path('delete/<int:game_id>/', views.game_delete_view, name="game_delete"),
    path('ims/', views.game_index_view, name="ims"),
    path('gamesapi/', views.gamesListCreate.as_view(), name="gamesapi_view_create"),
    path('gamesapi/<int:pk>', views.gamesRetrieveUpdateDestroy.as_view(), name="gamesapi_view_update"),
    
    path('game/<slug:slug>/', views.GameDetail.as_view(), name='game'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),

]

