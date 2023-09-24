from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('member_login/', views.member_login, name="member_login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_, name="logout"),

    path('profile/', views.profile, name="profile"),
    path('member_profile/<int:id>/', views.member_profile, name="member_profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('view_members/', views.view_members, name="view_members"),
    path('delete_member/<int:id>/', views.delete_member, name="delete_member"),

    path('view_books/', views.view_books, name="view_books"),
    path('book_profile/<int:id>', views.book_profile, name="book_profile"),
    path('addBook/', views.add_book, name="add_book"),
    path('edit_book/<int:id>/', views.edit_book, name="edit_book"),
    path('delete_book/<int:id>/', views.delete_book, name="delete_book"),

    path('issue_book/', views.issueBook, name="issue_book"),
    path('view_issued_books/', views.view_issued_books, name="view_issued_books"),
    path('book_returned/<int:id>', views.book_returned, name="book_returned"),
    path('delete_transaction/<int:id>', views.delete_transaction, name="delete_transaction"),
]