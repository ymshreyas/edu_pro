from django.contrib import admin
from django.urls import path
from edu_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.landing,name='landing'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('user_login/',views.user_login,name='user_login'),
    path('register/',views.register,name='register'),
    path('notification/',views.notification,name='notifications'),
    path('complaints/',views.complaints,name='complaints'),
    path('view_complaints/',views.view_complaints,name='view_complaints'),
    path('update_notification/',views.notification_update,name='update_notification'),
    path('take_attendance/', views.take_attendance, name='take_attendance'),
    path('view_attendance/', views.view_attendance, name='view_attendance'),
    path('update_cie/',views.update_cie,name='update_cie'),
    path('payments/',views.payment_view,name='payments')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)