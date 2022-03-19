"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ticket import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
                # Will be included into the below url
router.register('guests', views.ViewSets_Guest)
router.register('movies', views.ViewSets_Movie)
router.register('reservations', views.ViewSets_Reservation)

urlpatterns = [
    path('admin/', admin.site.urls),

    # using Djang   
    path('django/no_rest_no_model/', views.no_rest_no_model),
    path('django/no_rest_with_model/', views.no_rest_with_model),

    # Using RESt FrameWork

    # Using Function Based View (FBV)
    path('rest/FBV_LIST/', views.FBV_LIST),
    path('rest/FBV_PK/<int:pk>', views.FBV_PK),

    # Using Class Based View (CBV)
    path('rest/CBV_List/', views.CBV_List.as_view()),
    path('rest/CBV_PK/<int:pk>', views.CBV_PK.as_view()),
    
    # Using Mixins
    path('rest/Mixins_List/', views.Mixins_List.as_view()),
    path('rest/Mixins_PK/<int:pk>', views.Mixins_PK.as_view()),

    # Using Generics
    path('rest/Generics_List/', views.Generics_List.as_view()),
    path('rest/Generics_PK/<int:pk>', views.Generics_PK.as_view()),

    # Using ViewSets
    path('rest/', include(router.urls)),
    path('rest/', include(router.urls)),
    path('rest/', include(router.urls)),

    # Business Functions
    path('rest/find_movie/', views.find_movie),
    path('rest/new_reservation', views.new_reservation),
]
