from django.urls import path
from .views import (
    MebelsListView,
    MebelsDetailView,
    SubCategoryListView,
    CartItemListView, 
    CartItemDetailView, 
    LikeMebelView,
    UserLikesView,
    OrderListCreateView,
    OrderDetailView,
)



urlpatterns = [
    path('api/v2/mebels_list/', MebelsListView.as_view(), name='mebel-list'),
    path('api/v2/mebels_detail/<int:pk>/', MebelsDetailView.as_view(), name='mebel-detail'),
    path('api/v2/subcategories/', SubCategoryListView.as_view(), name='subcategory-list'),

    # Корзина
    path('cart/', CartItemListView.as_view(), name='cart-list'),
    # 
    path('cart/detail/<int:item_id>/', CartItemDetailView.as_view(), name='cart-detail'),

    # Лайки
    path('user/likes/', UserLikesView.as_view(), name='user-likes'),
    # 
    path('mebels/<int:mebel_id>/like/', LikeMebelView.as_view(), name='like-mebel'),

    # Заказы
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    # path('order-items/', OrderItemListCreateView.as_view(), name='order-item-list'),
    # path('order-items/<int:pk>/', OrderItemDetailView.as_view(), name='order-item-detail')
]


