
from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('<int:id>', views.index, name="index"),
    path(r'^favicon.ico$',
        RedirectView.as_view( # the redirecting function
            url=staticfiles_storage.url('img/favicon.ico'), # converts the static directory + our favicon into a URL
            # in my case, the result would be http://www.tumblingprogrammer.com/static/img/favicon.ico
        ),
        name="favicon" # name of our view
    ),
]
