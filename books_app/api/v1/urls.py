from django.urls import path

from .views import book, author, auth, comment

urlpatterns = [

    path('register', auth.RegisterView.as_view()),
    path('login', auth.LoginView.as_view()),
    path('refresh', auth.RefreshView.as_view()),
    path('authors', author.AuthorsView.as_view()),
    path('books', book.BooksView.as_view()),
    path('books/<int:book_id>', book.BookView.as_view()),
    path('books/<int:book_id>/comments', comment.CommentsView.as_view()),
    path('books/<int:book_id>/comments/<int:comment_id>', comment.CommentView.as_view())
]
