from django.urls import path

from .views import author, auth
from .views.book import rating, book, comment, favorite

urlpatterns = [
    # Auth
    path('register-author', auth.RegisterAuthorView.as_view()),
    path('register-user', auth.RegisterUserView.as_view()),
    path('confirm/<str:code>', auth.ConfirmRegisterView.as_view()),
    path('login', auth.LoginView.as_view()),
    path('refresh', auth.RefreshView.as_view()),
    path('recovery', auth.RecoveryUserView.as_view()),
    path('recovery/<str:code>', auth.RecoveryUserChangePasswordView.as_view()),

    # Authors
    path('authors', author.AuthorsView.as_view()),
    path('authors/<int:author_id>', author.AuthorView.as_view()),

    # Books
    path('books', book.BooksView.as_view()),
    path('books/<int:book_id>', book.BookView.as_view()),
    path('books/<int:book_id>/comments', comment.CommentsView.as_view()),
    path('books/<int:book_id>/comments/<int:comment_id>', comment.CommentView.as_view()),
    path('books/<int:book_id>/ratings', rating.RatingsView.as_view()),
    path('books/<int:book_id>/ratings/<int:rating_id>', rating.RatingView.as_view()),

    # Favorite
    path('books/favorite', favorite.RatingsView.as_view())
]
