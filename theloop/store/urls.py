from django.urls import path, include
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('category/<slug:cat_slug>/', CategoryView.as_view(), name='category'),
    path('collection/<slug:col_slug>/', CollectionView.as_view(), name='collection'),
    path('item/<slug:item_slug>/', ShowItem.as_view(), name='detail'),
    path('about/', About, name="about"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_user, name="logout"),
    path('bascet/', BascetView.as_view(), name="bascet"),
    path('saveorder/', saveorder, name="saveorder"),
    path('payment/', payment, name='payment')

]

