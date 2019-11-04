from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path
from .views import *
from django.conf import settings

urlpatterns = [
    path('main/<int:number_page>',main_page.as_view(),name='main_page'),
    path('category/<int:pk>/<number_page>',category,name='category'),
    path('product/<int:pk>',product, name='product'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('korzina/',go_to_korzina,name='korzina'),
    path('add',add,name='add'),
    path('my_products/<int:number_page>/<int:pk>',my_products,name='my_products'),
    path('edit/<int:pk>',edit,name='edit'),
    path('my_delete/<int:pk>',my_delete,name='my_delete'),
    path('add_to_korz/<int:id>',add_to_corz,name='add_to_korz'),
    path('del/<int:id>',Del,name='Del'),
    path('My_del/<int:id>',My_del,name='My_del'),
    path('register2/',register2,name='register2'),

]
