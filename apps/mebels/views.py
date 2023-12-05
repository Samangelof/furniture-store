from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .permissions import IsOwner, AdminOnlyCreate, IsOrderItemOwner
from .models import (
    Mebels,
    SubCategory,
    CartItem,
    Order,
    OrderItem
)
from .serializers import (
    MebelsSerializer,
    SubCategorySerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer
)


class MebelsListView(ListCreateAPIView):
    queryset = Mebels.objects.all()
    serializer_class = MebelsSerializer
    permission_classes = [AllowAny, AdminOnlyCreate]

class MebelsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Mebels.objects.all()
    serializer_class = MebelsSerializer
    permission_classes = [IsAdminUser]


# Подкатегории
class SubCategoryListView(ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [AllowAny, AdminOnlyCreate]

# •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
# Корзина
class CartItemListView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
# •••
    def get(self, request):
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart_items = CartItem.objects.filter(user=None)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
# •••
    def get_object(self, item_id):
        return get_object_or_404(CartItem, pk=item_id)


    def get(self, request, item_id):
        # Получить информацию о элементе корзины с заданным item_id
        cart_item = self.get_object(item_id)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id') # id товара
        quantity = request.data.get('quantity') # Количество

        if not product_id or not quantity:
            return Response({"error": "Укажите 'product_id' и 'quantity' для добавления товара в корзину."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Mebels.objects.get(pk=product_id)
        except Mebels.DoesNotExist:
            return Response({"error": "Указанный товар не найден."}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += quantity
        cart_item.save()

        return Response({"message": "Товар успешно добавлен в корзину."}, status=status.HTTP_201_CREATED)

    def delete(self, request, item_id):
        # Удалить элемент корзины с заданным item_id
        cart_item = self.get_object(item_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••


# •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
# Лайки
# Посмотреть все лайки
class UserLikesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        liked_products = Mebels.objects.filter(favorite__user=user)
        serializer = MebelsSerializer(liked_products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# Добавить / Удалить
class LikeMebelView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request, mebel_id):
        try:
            mebel = Mebels.objects.get(pk=mebel_id)
        except Mebels.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not mebel.is_liked:
            mebel.is_liked = True
            mebel.save()
            return Response({'message': 'Продукт добавлен в избранное'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Продукт уже в избранном'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, mebel_id):
        try:
            mebel = Mebels.objects.get(pk=mebel_id)
        except Mebels.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if mebel.is_liked:
            mebel.is_liked = False
            mebel.save()
            return Response({'message': 'Продукт удален из избранного'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Продукт не находится в избранном'}, status=status.HTTP_400_BAD_REQUEST)
# •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••



# •••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
# Заказы
class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class OrderItemListCreateView(ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny]


class OrderItemDetailView(RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsOrderItemOwner]