from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("events.urls")),
    path("members", include("django.contrib.auth.urls")),
    path("members/", include("members.urls")),
]

# Configure the Admin Titles
admin.site.site_header = "Spondy Club Admin"
admin.site.site_title = "Spondy Club"
admin.site.index_title = "Making Changes!"
