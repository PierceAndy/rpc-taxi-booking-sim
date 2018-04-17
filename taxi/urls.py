from django.urls import include, path

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('api/', include('booking.urls')),
]
