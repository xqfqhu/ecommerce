from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'account'
urlpatterns = [
    path('register/',views.account_register, name = 'register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name = 'activate'), 
    # recall that we pass uidb and token to for url in account_activation.html
    # so we'd have to speicify what the url looks like given these two arguments and associate the url with a view
    # in the view, we'd have to pass these two arguments to the view along with request
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.customLogin.as_view(), name = 'login'),
    path('logout/', views.customLogout.as_view(), name = 'logout'),
    path('profile/edit/', views.edit_details, name = 'edit_details'),
    path('profile/delete_user/', views.delete_user, name = 'delete_user'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name="account/user/delete_confirm.html"), name='delete_confirmation'),
    path('password_reset/', views.customPasswordResetView.as_view(), name = 'password_reset'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/', views.customPasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('password_reset/password_reset_email_confirm/', views.passwordResetEmailConfirm, name = 'password_reset_email_confirm'),
    path('password_reset_confirm/MjQ/set-password/passord_reset_complete/', views.passwordResetComplete, name = 'password_reset_complete'),
    path('add_address/', views.add_address, name = 'add_address'),
    path('addresses/', views.view_address, name = 'addresses'),
    path('delete_address/<slug:address_id>', views.delete_address, name = 'delete_address'),
    path('edit_address/<slug:address_id>', views.edit_address, name = 'edit_address'),
    path('set_default/<slug:address_id>', views.set_default, name = 'set_default'),
    path('dashboard/user_orders',views.account_user_orders, name = 'user_orders'),
    path('dashboard/user_wishlist',views.view_wishlist, name = 'user_wishlist'),
]
