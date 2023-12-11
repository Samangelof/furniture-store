from django.db import models


# ------------------------------------------------
# Информация о продуктах
class Mebels(models.Model):
    CATEGORY_CHOICES = (
        ('bedroom', 'Спальня'),
        ('living_room', 'Гостиная'),
        ('kitchen', 'Кухня'),
        ('dining_room', 'Мягкая мебель'),
        ('accessories', 'Аксессуары'),
        ('decorations', 'Декорации'),
    )


    name = models.CharField(verbose_name='Наименование', max_length=255, null=False, blank=False)
    description = models.CharField(verbose_name='Описание', max_length=255, null=True, blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, null=False, blank=False) 
    
    title_image = models.ImageField(upload_to='mebels/images/title_images', verbose_name='Основное изображение', null=True, blank=True)
    gallery_images = models.ManyToManyField('MebelImage', verbose_name='Изображения галереи', blank=True)

    category = models.CharField(verbose_name='Категория', max_length=255, choices=CATEGORY_CHOICES, null=True, blank=True)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, verbose_name='Подкатегория', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мебель"
        verbose_name_plural = "Мебель"


class MebelImage(models.Model):
    mebel = models.ForeignKey(Mebels, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Изображение', upload_to='mebels/images/', null=True, blank=True)

    class Meta:
        verbose_name = "Изображение мебели"
        verbose_name_plural = "Изображения мебели"


class SubCategory(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=255)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

# ------------------------------------------------
# Управление складскими запасами
class Order(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('confirmed', 'Подтвержден'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
    ]

    user = models.ForeignKey('auths.CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


    def __str__(self):
        return f'Заказ #{self.pk}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    mebel = models.ForeignKey(Mebels, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Заказанное количество')
    delivered_quantity = models.PositiveIntegerField(default=0, verbose_name='Доставленное количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    is_delivered = models.BooleanField(default=False, verbose_name='Доставлено')

    def __str__(self):
        return f'{self.quantity} x {self.mebel.name} в заказе #{self.order.pk}'

    
    class Meta:
        verbose_name = "Подробности заказа"
        verbose_name_plural = "Подробности заказов"


# Корзина
class CartItem(models.Model):
    product = models.ForeignKey('Mebels', on_delete=models.CASCADE, verbose_name='Продукт', blank=False)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество', blank=False)
    user = models.ForeignKey('auths.CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь', blank=False)

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

    def __str__(self):
        return f"Корзина - {self.quantity} шт. {self.product.name}"



# Избранное / Лайки
class Favorite(models.Model):
    user = models.ForeignKey('auths.CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь')
    mebel = models.ForeignKey(Mebels, on_delete=models.CASCADE, verbose_name='Избранное')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные продукты'

    def __str__(self):
        return f"{self.user} - {self.mebel}"