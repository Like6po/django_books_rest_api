from django.urls import path

from .views import author, auth
from .views.book import rating, book, comment, favorite

urlpatterns = [
    # Auth
    path('register-author', auth.RegisterAuthorView.as_view(), name="register_author"),
    path('register-user', auth.RegisterUserView.as_view(), name="register_user"),
    path('confirm/<str:code>', auth.ConfirmRegisterView.as_view(), name="confirm"),
    path('login', auth.LoginView.as_view(), name="login"),
    path('refresh', auth.RefreshView.as_view(), name="refresh"),
    path('recovery', auth.RecoveryUserView.as_view(), name="recovery"),
    path('recovery/<str:code>', auth.RecoveryUserChangePasswordView.as_view(), name="recovery_code"),

    # Authors
    path('authors', author.AuthorsView.as_view(), name="authors"),
    path('authors/<int:author_id>', author.AuthorView.as_view(), name="authors_detail"),

    # Books
    path('books', book.BooksView.as_view(), name="books"),
    path('books/<int:book_id>', book.BookView.as_view(), name="books_detail"),
    path('books/<int:book_id>/comments', comment.CommentsView.as_view(), name="books_comments"),
    path('books/<int:book_id>/comments/<int:comment_id>', comment.CommentView.as_view(), name="books_comments_detail"),
    path('books/<int:book_id>/ratings', rating.RatingsView.as_view(), name="books_ratings"),
    path('books/<int:book_id>/ratings/<int:rating_id>', rating.RatingView.as_view(), name="books_ratings_detail"),

    # Favorite
    path('books/favorites', favorite.FavoriteView.as_view(), name="favorites")
]
