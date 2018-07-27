
from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('<int:id>/<int:act>/<int:scene>/<str:word>', views.index, name="index"),
    # path('word/<str:word>', views.index, name="index"),
    path('<int:id>', views.index, name="index"),
    path('comment/<int:id>', views.comment, name="comment"),
    path('comments/<int:id>', views.comments, name="comments"),

    path(r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('img/favicon.ico'), # converts the static directory + our favicon into a URL
        ),
        name="favicon"
    ),
]
