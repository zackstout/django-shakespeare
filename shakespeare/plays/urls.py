
from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('<int:id>', views.index, name="index"),
    path('comment/<int:id>', views.comment, name="comment"),
    # path('addcomment/<int:id>', views.addcomment, name="addcomment"),

    path(r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('img/favicon.ico'), # converts the static directory + our favicon into a URL
        ),
        name="favicon"
    ),
]
