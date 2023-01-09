from django.contrib import admin
from .models import *


@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_published', 'discount', 'quantity', 'time_create')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("name", "color", "size")}
    save_as = True
    save_on_top = True


class CatLine(admin.TabularInline):
    model = Clothes
    extra = 5

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    inlines = [CatLine]
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name", )}


# class ProvLine(admin.TabularInline):
#     model = Shipment
#
# @admin.register(Provider)
# class ProviderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     list_display_links = ('id', 'name')
#     search_fields = ('name',)
#     prepopulated_fields = {"slug": ("name",)}
#     inlines = [ProvLine]


class OrdLine(admin.TabularInline):
    model = ArticleForOrd
    extra = 1

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'user', 'is_paid', 'is_took')
    search_fields = ('user', 'date', 'id', )
    inlines = [OrdLine]


# class ShipLine(admin.TabularInline):
#     model = ArticleForShip
#     extra = 5
# @admin.register(Shipment)
# class ShipmentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'provider', 'date', 'is_paid', 'is_took')
#     list_display_links = ('id', 'provider')
#     search_fields = ('name', 'id')
#     list_editable = ('is_paid', 'is_took')
#     list_filter = ('provider', 'date')
#     inlines = [ShipLine]


class CollLine(admin.TabularInline):
    model = Clothes
    extra = 5
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


# admin.site.register(ArticleForShip)
admin.site.register(ArticleForOrd)
