from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . views import *
from .context_processors import all_categories

urlpatterns = [
   path('',DisplayProductHomePage.as_view(),name='index'),
   path('register',RegisterView.as_view(),name = 'register'),
   path('login',LoginView.as_view(),name='login'),
   path('logout',LogoutView.as_view(),name='logout'),
   path('list-product/',ProductView.as_view(),name="list_product"),
   path('list-product/<str:category_slug>',ProductView.as_view(),name="list_product_category"),
   path('get-all-categories',all_categories,name="get_all_categories"),
   path('product-detail/<int:pk>/',ProductDetail.as_view(),name='product_detail'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 