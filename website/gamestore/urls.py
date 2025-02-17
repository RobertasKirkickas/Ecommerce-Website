from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('profile/', views.profile, name="profile"),
    path('contact/success/', views.contact_success_view, name='contact-success'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order_summary'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('protected/', views.ProtectedView.as_view(), name='protected'),
    path('create/', views.game_create_view, name="game_create"),
    path('list/', views.game_list_view, name="game_list"),
    path('search/', views.SearchView.as_view(), name="search"),
    path('update/<int:game_id>/', views.game_update_view, name="game_update"),
    path('delete/<int:game_id>/', views.game_delete_view, name="game_delete"),
    path('ims/', views.game_index_view, name="ims"),
    path('gamesapi/', views.gamesListCreate.as_view(), name="gamesapi_view_create"),
    path('gamesapi/<int:pk>', views.gamesRetrieveUpdateDestroy.as_view(), name="gamesapi_view_update"),
    path('game/<slug:slug>/', views.GameDetail.as_view(), name='game'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-single-from-cart/<slug>/', views.remove_single_from_cart, name='remove_single_from_cart'),
    path('delete-profile/<str:username>/', views.delete_profile, name='delete_profile'), 
    path('profile-confirm-delete/', views.profile_confirm_delete, name='profile_confirm_delete'), 

]

