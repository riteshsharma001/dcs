from django.contrib import admin
from django.urls import path, include
from webapp.views import LoginActivityList
from webapp.views import DocumentSubmitView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login-activity/', LoginActivityList.as_view(), name='login-activity')
    path('DocumentSubmit/', DocumentSubmitView.as_view(), name='Document-Submit')
]
