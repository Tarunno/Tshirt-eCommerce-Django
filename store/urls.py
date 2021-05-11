from django.urls import path
from .import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.store, name='store'),
    path('store/', views.store, name='store'),
    path('cart/<str:action>', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('category/<id>/', views.category_items, name='category'),
    path('search/<str:query>', views.search, name='search'),
    path('product/<int:id>/', views.view_product, name='product'),
    path('rating_update/', views.rating_update, name='rating_update'),
    path('update_review/', views.update_review, name='update_review'),
    path('order_placed/', views.order_placed, name="order_placed"),
    path('custom/', views.custom, name="custom")

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
