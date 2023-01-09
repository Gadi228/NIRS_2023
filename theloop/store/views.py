from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.db.models import F
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView

from .forms import RegisterUserForm, LoginUserForm
from .models import Clothes, Category, Orders, ArticleForOrd
from .utils import DataMixin


# Create your views here.


class IndexView(DataMixin, ListView):
    model = Clothes
    template_name = "store/index.html"
    context_object_name = 'clothes'

    def get_context_data(self, *, object_list=None, **kwargs):
        pricesdisc = [0, 0, 0, 0]
        context = super().get_context_data(**kwargs)
        # allclothes = Clothes.objects.all()
        # for clothes in allclothes:
        #     if clothes.collection:
        #         clothes.pricedisc = clothes.price * (100 - max(clothes.discount, clothes.cat.discount, clothes.collection.discount))/100
        #     else:
        #         clothes.pricedisc = clothes.price * (100 - max(clothes.discount, clothes.cat.discount))/100
        #         clothes.save()
        first4 = Clothes.objects.filter(quantity__gte=1, is_published=True).order_by('-discount')[:4]
        c_def = self.get_user_context(title="Главная страница", first4=first4, pricesdisc=pricesdisc)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Clothes.objects.filter(
            quantity__gte=1, is_published=True
        ).order_by('-time_update')


class CollectionView(DataMixin, ListView):
    model = Clothes
    template_name = "store/category.html"
    slug_url_kwarg = 'col_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Коллекция")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Clothes.objects.filter(
            quantity__gte=1, is_published=True, collection__slug=self.kwargs['col_slug']
        ).order_by('-time_update')


class CategoryView(DataMixin, ListView):
    model = Clothes
    template_name = "store/category.html"
    slug_url_kwarg = 'cat_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Категории")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Clothes.objects.filter(
            quantity__gte=1, is_published=True, cat__slug=self.kwargs['cat_slug']
        ).order_by('-time_update')


class ShowItem(DataMixin, DetailView):
    model = Clothes

    template_name = 'store/item.html'
    slug_url_kwarg = 'item_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # form_class = OrdersUserForm
        c_def = self.get_user_context(title="Главная страница", ) #form=form_class)
        return dict(list(context.items()) + list(c_def.items()))


def About(request):
    return render(request, 'store/about.html')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class BascetView(DataMixin, ListView):
    model = Clothes
    template_name = 'store/bascet.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ord = Orders.objects.get(user=self.request.user, is_paid=False)
        elements = user_ord.articleforord_set.all()
        money = 0
        for el in elements:
            if el.clothes.pricedisc:
                money += el.clothes.pricedisc * el.quantity
            else:
                money += el.clothes.price * el.quantity
        c_def = self.get_user_context(title="Авторизация", elements=elements, money=money)
        return dict(list(context.items()) + list(c_def.items()))


def saveorder(request):
    quant = request.POST['quantity']
    prod = Clothes.objects.get(slug=request.POST['prod'])
    order = request.user.orders_set.order_by('date').last()

    if not order or order.is_paid:
        order = Orders.objects.create(user=request.user)
    else:
        art = order.articleforord_set.filter(clothes__slug=prod.slug).last()
        if art:
            quant1 = int(quant) + art.quantity
            if quant1 > prod.quantity:
                return already(request, "Вы уже добавили в корзину максимальное количество данного товара")
            art.quantity = quant1
            art.save()
            return redirect('detail', item_slug=prod.slug)
    element = ArticleForOrd.objects.create(clothes=prod, order=order, quantity=quant)
    element.save()
    return redirect('detail', item_slug=prod.slug)


def payment(request):

    ord = request.user.orders_set.get(user=request.user, is_paid=False)
    cloth = ord.articleforord_set.all()
    for cl in cloth:
        cl.clothes.quantity -= cl.quantity
        cl.clothes.save()
    ord.is_paid = True
    ord.save()
    return redirect('home')

def already(request, str):
    context = {'exeption': str, }
    return render(request, 'store/mistake.html', context)

