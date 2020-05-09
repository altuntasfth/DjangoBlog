import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Menu, Content, CImages
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactForm, ContactFormMessage
from product.models import Product, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdate = Product.objects.filter(status=True)[:3]
    category = Category.objects.all()
    menu = Menu.objects.all()
    dayproduct = Product.objects.filter(status=True)[:6]
    lastproduct = Product.objects.filter(status=True).order_by('-id')[:6]
    randomproduct = Product.objects.filter(status=True).order_by('?')[:3]
    context = {'setting': setting,
               'page': 'home',
               'category':  category,
               'menu':  menu,
               'sliderdata': sliderdate,
               'dayproducts': dayproduct,
               'lastproducts': lastproduct,
               'randomproducts': randomproduct}
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category, }
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category, }
    return render(request, 'referanslarimiz.html', context)


def iletisim(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Mesaj başarı ile gönderilmiştir.')
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    category = Category.objects.all()
    context = {'setting': setting,
               'form': form,
               'category': category, }
    return render(request, 'iletisim.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products': products,
               'category': category,
               'categorydata': categorydata, }
    return render(request, 'products.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    try:
        product = Product.objects.get(pk=id)
        images = Images.objects.filter(product_id=id)
        comments = Comment.objects.filter(product_id=id, status='True')
        context = {'category': category,
                   'product': product,
                   'images': images,
                   'comments': comments, }
        return render(request, 'product_detail.html', context)
    except:
        messages.warning(request, 'Hata! İlgili içerik bulunamadı.')
        link = '/error'
        return HttpResponseRedirect(link)


def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            #catid = form.cleaned_data['catid']
            query = form.cleaned_data['query']
            #return HttpResponse(catid)

            #if catid == 0:
            products = Product.objects.filter(title__icontains=query)
            #else:
                #products = Product.objects.filter(title__icontains=query, category_id=catid)

            #return HttpResponse(products)
            context = {'category': category,
                       'products': products, }
            return render(request, 'products_search.html', context)

    return HttpResponseRedirect('/')


def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Kullanıcı adı yada şifre yanlış!')
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {'category': category, }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form, }
    return render(request, 'signup.html', context)


def error(request):
    category = Category.objects.all()
    menu = Menu.objects.all(),
    context = {'category': category,
               'menu': menu}
    return render(request, 'error.html', context)