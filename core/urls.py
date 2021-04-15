from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='homepage'),
	path('calendar/', views.calendar, name='calendar'),
	path('account/', views.account, name='account'),
	path('potential-client/', views.client_list, name='client_list'),
	path('clients/', views.clients, name='clients'),
	path('client/<slug:slug>/', views.client_detail, name='client_detail'),
	path('delete-comment/<comment_id>/<client_id>/', views.del_comment, name='delete_comment'),
	path('update_client/<id>/', views.update_client, name='update_client'),
	path('update_user/', views.update_user, name='update_user'),
	path('change_pass', views.update_pass, name='change_pass'),
	path('sucs_change/', views.sucsch, name='sucs_change'),
	path('new_client/', views.new_client, name='new_client'),
]
