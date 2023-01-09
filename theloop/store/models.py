from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Clothes(models.Model):
    name = models.CharField(max_length=100, verbose_name="Заголовок")
    collection = models.ForeignKey('Collection', on_delete=models.PROTECT, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    color = models.CharField(max_length=30, verbose_name="Цвет")
    price = models.PositiveIntegerField(verbose_name="Цена")
    discount = models.IntegerField(default=0, verbose_name="Скидка в процентах")
    pricedisc = models.IntegerField(auto_created=True, default=0, verbose_name="Цена со скидкой")
    photo = models.ImageField(upload_to="article/", verbose_name="Фото")
    content = models.TextField(default="", blank=True, verbose_name="Описание")
    size = models.PositiveIntegerField(verbose_name="Размер")
    is_published = models.BooleanField(default=True, verbose_name="Выставить")
    quantity = models.PositiveIntegerField(default=0, blank=True, verbose_name="Остаток на складе")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    def __str__(self):
        return self.name + ' ' + self.color

    def get_absolute_url(self):
        return reverse('detail', kwargs={'item_slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['time_create']


class Collection(models.Model):
    name = models.CharField(max_length=100, verbose_name="Коллекция")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    discount = models.IntegerField(default=0, verbose_name="Скидка на коллекцию")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('collection', kwargs={'col_slug': self.slug})

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    discount = models.IntegerField(default=0, verbose_name="Скидка на каталог")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Provider(models.Model):
    name = models.CharField(max_length=150, verbose_name="Поставщик")
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['id']


class ArticleForShip(models.Model):
    clothes = models.ForeignKey('Clothes', on_delete=models.PROTECT, verbose_name="Одежда")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    shipment = models.ForeignKey('Shipment', on_delete=models.PROTECT)

    def __str__(self):
        return self.clothes.name + str(self.quantity)

    class Meta:
        verbose_name = 'Артикль поставки'
        verbose_name_plural = 'Артикли поставок'
        ordering = ['-id']


class Shipment(models.Model):
    provider = models.ForeignKey('Provider', on_delete=models.PROTECT, verbose_name="Поставщик")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата поставки")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    is_took = models.BooleanField(default=False, verbose_name="Оприходован")

    def __str__(self):
        return self.provider.name + str(self.date)

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'
        ordering = ['id']


class ArticleForOrd(models.Model):
    clothes = models.ForeignKey('Clothes', on_delete=models.PROTECT, verbose_name="Одежда")
    quantity = models.PositiveIntegerField(default=0, blank=True, verbose_name="Количество")
    order = models.ForeignKey('Orders', null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.clothes.name + str(self.quantity)

    class Meta:
        verbose_name = 'Артикль покупки'
        verbose_name_plural = 'Артикли покупок'
        ordering = ['-id']


class Orders(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата покупки")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Покупатель")
    is_paid = models.BooleanField(default=False, verbose_name="Оплата")
    is_took = models.BooleanField(default=False, verbose_name="Получен")

    def __str__(self):
        return self.user.username + str(self.date)

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['is_took', 'id']
