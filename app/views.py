from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models  import Sum
# from django.utils import timezone
from app.models import Members, Book, Transaction
from app.forms import IssueBookForm
from datetime import date, datetime
import requests

# Create your views here

def index(request):
    return render(request, 'index.html')

def admin_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.info(request, "Invalid Username.")
            return redirect('/admin_login/')
        
        if not user.is_superuser:
            messages.info(request, 'Not an Admin.')
            return redirect('/admin_login/')
        login(request, user)
        return redirect('/view_members/')
        
    return render(request, 'admin_login.html')

def member_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)

        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid Username")
            return redirect('/member_login/')

        user = authenticate(request, username=username, password=password)
        print(user)

        if user is None:
            messages.info(request, "Invalid Password.")
            return redirect('/member_login/')
        
        if user.is_superuser:
            messages.info(request, 'You are an Admin. Please login through admin portal.')
            return redirect('/')
        
        login(request, user)
        return redirect('/profile/')
        
    return render(request, 'member_login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_no = request.POST['phone_no']
        image = request.FILES.get('image') or None
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.info(request, 'Password do not match.')
            return redirect('/register/')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already in use.')
            return redirect('/register/')
        
        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        member = Members(user=user, phone_no=phone_no, image=image)
        member.user.save()
        member.save()
        messages.info(request, 'You have successfully registered.')
        return redirect('/member_login/')
    return render(request, 'register.html')

@login_required(login_url="/member_login/")
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='/admin_login/')
def member_profile(request, id):
    member = Members.objects.get(id=id)
    return render(request, 'member_profile.html', {'member': member})

@login_required(login_url='/member_login/')
def edit_profile(request):
    member = Members.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        member.user.email = request.POST['email']
        member.user.first_name = request.POST['first_name']
        member.user.last_name = request.POST['last_name']
        member.phone_no = request.POST['phone_no']
        if request.FILES.get('image'):
            member.image = request.FILES.get('image')

        member.user.save()
        member.save()
        messages.info(request, 'Your changes has been successful.')
        return redirect('/profile/')
    return render(request, 'edit_profile.html', {'member': member})

@login_required(login_url='/admin_login/')
def issueBook(request):
    if request.method=='POST':
        form = IssueBookForm(request.POST)
        if form.is_valid:
            member_id = request.POST.get('name2')
            isbn = request.POST.get('isbn2')
            amount_paid = request.POST.get('amount_paid')

            debt = Transaction.objects.filter(member_id=member_id).aggregate(totalDebt=Sum('amount_remaining')).get('totalDebt') or 0
            book = Book.objects.filter(isbn=isbn)[0]

            if debt>500:
                messages.info(request, 'Cannot issue book as total debt exceeds 500.')
            elif book.price>500:
                messages.info(request, 'Book price exceeds 500.')
            else:
                amount_remaining = book.price - int(amount_paid)
                issue_book = Transaction.objects.create(
                member_id=member_id,
                isbn=isbn,
                amount_paid=amount_paid,
                amount_remaining=amount_remaining,
                issued_date = date.today(),
                )
                issue_book.save()
                return redirect('/view_issued_books/')
    else:
        form = IssueBookForm()
    return render(request, 'IssueBook.html', {'form': form})

@login_required(login_url='/admin_login/')
def view_issued_books(request):
    transactions = Transaction.objects.all()
    details = []
    for transaction in transactions:
        members = list(Members.objects.filter(user=transaction.member_id))
        book = list(Book.objects.filter(isbn=transaction.isbn))
        for i in range(len(book)):
            detail = (members[i].user.get_full_name(), book[i].title, book[i].isbn, transaction.amount_paid, transaction.amount_remaining, transaction.issued_date, transaction.return_date, transaction.id)
            details.append(detail)

    return render(request, 'view_issued_book.html', {'details': details})

@login_required(login_url='/admin_login/')
def book_returned(request, id):
    transaction = Transaction.objects.get(id=id)
    transaction.return_date = date.today()
    transaction.save()
    return redirect('/view_issued_books/')

@login_required(login_url='/admin_login/')
def add_book(request):
    if request.method=='POST':
        bookId = request.POST['bookid']
        title = request.POST['title']
        authors = request.POST['authors']
        isbn = request.POST['isbn']
        isbn13 = request.POST['isbn13'] or 0
        language = request.POST['language']
        num_pages = request.POST['num_pages'] or 0
        publication_date = request.POST.get('publication_date')
        publisher = request.POST['publisher']
        price = int(request.POST['price'])

        book = Book.objects.create(
            bookId=bookId,
            title=title,
            authors=authors,
            isbn=isbn,
            isbn13=isbn13,
            language=language,
            num_pages=num_pages,
            publication_date=publication_date,
            publisher=publisher,
            price=price
        )

        book.save()
        messages.info(request, "Book has been added.")

    return render(request, 'add_book.html')

@login_required(login_url='/admin_login/')
def edit_book(request, id):
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        book.bookId = request.POST['bookid']
        book.title = request.POST['title']
        book.authors = request.POST['authors']
        book.isbn = request.POST['isbn']
        book.isbn13 = request.POST['isbn13']
        book.language = request.POST['language']
        book.num_pages = request.POST['num_pages']
        book.publisher = request.POST['publisher']
        book.price = request.POST['price']

        if request.POST.get('publication_date'):
            book.publication_date = request.POST.get('publication_date')

        book.save()
        messages.info(request, 'Your changes has been successful.')
        return redirect(f'/book_profile/{book.id}')
    return render(request, 'edit_book.html', {'book': book})

def book_profile(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'book.html', {'book': book})

def view_object(request, model):
    object = model.objects.all()
    paginator = Paginator(object, 25)

    page = request.GET.get('page')
    pagination = paginator.get_page(page)
    
    return pagination

@login_required(login_url='/admin_login/')
def view_members(request):
    pagination = view_object(request, Members)
    return render(request, 'view_members.html', {'pagination': pagination})

@login_required(login_url='/admin_login/')
def view_members_detail(request, id):
    member = Members.objects.get(id=id)
    return render(request, 'member_detail', {'member': member})

def view_books(request):
    pagination = view_object(request, Book)
    admin = False
    if request.user.is_superuser:
        admin = True
    return render(request, 'view_books.html', {'pagination': pagination, 'admin': admin})

@login_required(login_url='/admin_login/')
def delete_member(request, id):
    member = Members.objects.get(id=id)
    member.user.delete()
    member.delete()
    return redirect('/view_members/')

@login_required(login_url='/admin_login/')
def delete_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('/view_books/')

@login_required(login_url='/admin_login/')
def delete_transaction(request, id):
    transaction = Transaction.objects.get(id=id)
    transaction.delete()
    return redirect('/view_issued_books/')

def logout_(request):
    logout(request)
    return redirect('/')

def integration(request):
    url = f' https://frappe.io/api/method/frappe-library?page=2&title=and'
    data = requests.get(url).json()['message']
    for d in data:
        dateobj = datetime.strptime(d['publication_date'], '%m/%d/%Y')
        try:
            book = Book.objects.create(
                bookId=d['bookID'],
                title = d['title'],
                authors=d['authors'],
                average_ratings = d['average_ratings'],
                isbn=d['isbn'],
                isbn13=d['isbn13'],
                language=d['language_code'],
                num_pages = d['num_pages'],
                ratings_count=d['ratings_count'],
                text_reviews_count=d['text_reviews_count'],
                publication_date=dateobj,
                publisher=d['publisher']
            )
        except:
            continue
    return render('/view_books/')