from django.urls import include, path
from . import views

urlpatterns = [

    path('registration/',views.registration, name='registration'),

    path('login/',views.login_page, name='login'),

    path('logout/',views.logoutUser, name='logout'),

    path('',views.home, name='home'),

    path('analyze_review/',views.review, name='review'), #Rownok
    
    path('dashboard/', views.userPage, name = 'dashboard'),

    path('adminpanel/', views.adminpanel, name = 'adminpanel'),

    path('client/<str:pk_test>/', views.client , name = 'client'), 

    path('createorder/', views.createorder, name = 'createorder'),

    path('files/',views.files, name = 'files'),

    # path('upload_review/', views.upload_review, name = 'upload_review'),



]
