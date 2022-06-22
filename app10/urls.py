
from django.urls import path
from app10.views import *
from . import views

urlpatterns = [
    path('', homeview.as_view(),name='home'),
    path('register/', RegisterView.as_view(),name='register'),
    path('login/',UserLogin.as_view(),name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('category/',AddCategoryView.as_view(),name='category'),
    path('subscription/',AddSubscriptionView.as_view(),name='subscription'),
    path('list/category/',CategorylistView.as_view(),name='catlist'),
    path('list/subscription/',SubscriptionListView.as_view(),name='sublist'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('pay/',PaymentView.as_view(), name='pay'),
    path('book/<int:pk>', SubBookView.as_view(), name='book'),
    path('feature', featureview.as_view(),name='feature'),
    path('aboutus', aboutusview.as_view(),name='aboutus'),
    path('workinghours', workinghoursview.as_view(),name='workinghours')


]
