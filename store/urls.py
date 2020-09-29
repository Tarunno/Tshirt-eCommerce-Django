from django.urls import path
from .import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.store, name='store'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('about/', views.about, name='about'),
    path('update_item/', views.update_item, name='update_item'),
    path('signup/', views.signup, name='signup'),
    path('category/<id>/', views.category_items, name='category'),
    path('search/<str:query>', views.search, name='search'),
    path('product/<int:id>/', views.view_product, name='product'),
    path('rating_update/', views.rating_update, name='rating_update'),
    path('update_review/', views.update_review, name='update_review')

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
