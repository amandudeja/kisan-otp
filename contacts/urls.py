from django.urls import path
from contacts import views

app_name = 'contacts'

urlpatterns = [

	path('<int:contact_id>',views.detail,name='detail'),
	path('<int:contact_id>/send/',views.sendform,name='send'),
	path('sentmesseages/',views.sentmessages,name='sentmesseages'),


]