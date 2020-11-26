from django.urls import path,re_path
from django.conf.urls import url
from clientmanager import views
import xadmin

urlpatterns = [
    path('',views.index),
    path('index/',views.index),

    path('pictures/',views.pictures),
    path('pictures/page/<int:num>/',views.pictures),

    path('picture/',views.picture),
    path('picture/<str:name>/<str:time>/<path:path>/', views.picture),
    path('xadmin/', xadmin.site.urls),
    path('test/<int:age>/<str:name>/<path:msg>/',views.test),
]
handler404 = views.page_not_found
