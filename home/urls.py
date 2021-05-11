from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('contact/',views.contact),
    path('home/',views.index),
    path('register/', views.register, name="register"),
    path('login/',views.login,name = "login"),
    path('userlog/<str:username>/', views.userlog,name = "userlog"),
    path('setting/<str:username>/',views.check),
    path('admin/<str:username>/',views.admin,name = "admin"),
    path('family/',views.family, name = "family"),
    path('compa/',views.compa),
    path('spec/',views.spec),
    path('searchct/',views.searchcity),
    path('ctresult/',views.ctresult),
    path('logre/',views.loginrequire),
    path('huygoi/<str:username>/',views.cancelpack),
    path('avaipack/<str:username>/',views.packavai,name = "avaipack"),
    path('regispack/<str:username>-<int:pid>/',views.regispack),
    path('extend/<str:username>/',views.extend),
    path('tracuu/<str:username>/',views.research),
    path('timkiem/',views.find)
]