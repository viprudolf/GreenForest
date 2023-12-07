from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm
from .models import CartItem
from django.shortcuts import redirect

from django.shortcuts import render
from .models import Product
from django.core.mail import send_mail
from .forms import ContactForm
@login_required(login_url='login')
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        # Обработка формы
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'Новая заявка с сайта'

            # Строка с информацией о товарах
            cart_info = '\n'.join(
                [f'{item.product.name} - {item.quantity} шт. - {item.product.price * item.quantity} Рублей' for item in
                 cart_items])

            # Создание сообщения
            message = f'Имя: {form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]}\n'
            message += f'Email: {form.cleaned_data["email_address"]}\n'
            message += f'Номер телефона: {form.cleaned_data["number_telefon"]}\n'
            message += f'Город: {form.cleaned_data["city"]}\n'
            message += f'Улица: {form.cleaned_data["address"]}\n'
            message += f'Сообщение: {form.cleaned_data["message"]}\n\n'
            message += f'Общая сумма товара: {total_price} Рублей\n\n'
            message += f'Товары в корзине:\n{cart_info}'

            from_email = 'rudchenko.rudchenko27@gmail.com'
            recipient_list = ['vip.rudolf_n@mail.ru']

            send_mail(subject, message, from_email, recipient_list)

            # Дополнительная логика после успешной обработки формы
            # Например, редирект или другие действия
            return render(request, 'blog/success.html')  # Создайте шаблон success.html

    else:
        form = ContactForm()

    return render(request, 'blog/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'form': form})





def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product,

                                                        user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')



def layout(request):
    products = Product.objects.all()

    return render(request, 'blog/layout.html', {'products': products})


def about(request):
    return render(request, 'blog/about.html')


# страница пользователя
def me(request):
    # если не авторизован, то редирект на страницу входа
    if not request.user.is_authenticated:
        return redirect('login')
    # рендерим шаблон и передаем туда объект пользователя
    return render(request, 'blog/me.html', {'user': request.user})


# выход
def doLogout(request):
    # вызываем функцию django.contrib.auth.logout и делаем редирект на страницу входа
    logout(request)
    return redirect('login')


# страница входа
def loginPage(request):
    # инициализируем объект класса формы
    form = LoginForm()

    # обрабатываем случай отправки формы на этот адрес
    if request.method == 'POST':

        # заполянем объект данными, полученными из запроса
        form = LoginForm(request.POST)

        # проверяем валидность формы
        if form.is_valid():
            # пытаемся авторизовать пользователя
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                # если существует пользователь с таким именем и паролем,
                # то сохраняем авторизацию и делаем редирект
                login(request, user)
                return redirect('me')
            else:
                # иначе возвращаем ошибку
                form.add_error(None, 'Неверные данные!')

    # рендерим шаблон и передаем туда объект формы
    return render(request, 'blog/login.html', {'form': form})


# регистрация
def registerPage(request):
    # инициализируем объект формы
    form = RegisterForm()

    if request.method == 'POST':
        # заполняем объект данными формы, если она была отправлена
        form = RegisterForm(request.POST)

        if form.is_valid():
            # если форма валидна - создаем нового пользователя
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            return redirect('login')
    # ренедерим шаблон и передаем объект формы
    return render(request, 'blog/registration.html', {'form': form})


# фильтр


from django.db.models import Q

def product_list(request):
    products = Product.objects.all()

    # Обработка поиска по имени
    search_query = request.GET.get('search_query')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Обработка поиска по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price and max_price:
        # Если указаны и минимальная, и максимальная цена
        products = products.filter(price__range=(min_price, max_price))
    elif min_price:
        # Если указана только минимальная цена
        products = products.filter(price__gte=min_price)
    elif max_price:
        # Если указана только максимальная цена
        products = products.filter(price__lte=max_price)

    context = {
        'products': products,
    }

    return render(request, 'blog/product_search.html', context)


