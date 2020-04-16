
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactForm, ContactFormMessage
from product.models import Product, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdate = Product.objects.all()[:3]
    category = Category.objects.all()
    dayproduct = Product.objects.all()[:6]
    lastproduct = Product.objects.all().order_by('-id')[:6]
    randomproduct = Product.objects.all().order_by('?')[:3]
    context = {'setting': setting,
               'page': 'home',
               'category':  category,
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
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'category': category,
               'product': product,
               'images': images,
               'comments': comments, }
    return render(request, 'product_detail.html', context)

