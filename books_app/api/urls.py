from django.urls import path

# Serializers define the API representation.
from api import views

# Routers provide an easy way of automatically determining the URL conf.


urlpatterns = [

    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('authors', views.AuthorsView.as_view()),
    path('books', views.BooksView.as_view()),
    path('books/<int:book_id>', views.BookView.as_view()),
]
