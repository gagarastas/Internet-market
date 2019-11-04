from django.shortcuts import render,render_to_response,redirect
from django.views import View
from .models import Product,korzina
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.core.paginator import Paginator
from .form import *
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
import re


class main_page(View):
    def get(self,request,number_page):
        stuff=Product.objects.all()
        username=auth.get_user(request).username
        q=request.GET.get('q')
        if q is not None:
            stuff=stuff.filter(name__icontains=q)
        id=request.GET.get('id')
        if id is not None:
            all_products_in_korzina=korzina.objects.all()
            user = auth.get_user(request)
            if user.is_authenticated:
                product=Product.objects.get(id=id)
                check=all_products_in_korzina.filter(user=user.id,product=product)
                if not check:
                    korz=korzina.objects.create(user=user,product=product)
                    return HttpResponse(status=200)
            else: return redirect('login')
        curent_page = Paginator(stuff, 6)
        if number_page>curent_page.num_pages:
            number_page=curent_page.num_pages
        stuff=curent_page.page(number_page)
        return render(request,'main_page.html',context={'stuff':stuff, 'username':username,'filter':q})


def category(request,pk,number_page):
    all_stuff=Product.objects.all()
    username=auth.get_user(request).username
    q=request.GET.get('q')
    if pk==0:
        stuff=all_stuff
    if pk==1:
        stuff = all_stuff.filter(category='telephone')
    if pk==2:
        stuff=all_stuff.filter(category='tablet')
    if pk==3:
        stuff=all_stuff.filter(category='laptop')
    if q is not None:
        stuff=stuff.filter(name__icontains=q)
    curent_page=Paginator(stuff,6)
    if int(number_page)>curent_page.num_pages:
        number_page = curent_page.num_pages
    stuff=curent_page.page(number_page)
    return render(request, 'main_page.html', context={'stuff': stuff,'username':username,'pk':pk,'filter':q})

def product(request,pk):
    all_stuff=Product.objects.all()
    username=auth.get_user(request).username
    product=all_stuff.get(pk=pk)
    return render(request,'product.html',context={'product':product,'username':username})

def go_to_korzina(request):
    user_id=auth.get_user(request).id
    all_products=korzina.objects.all()
    filter_products=all_products.filter(user=user_id)
    q=request.GET.get('q')
    return render(request,'korzina.html',context={'filter_products':filter_products})

def login(request):
    context={}
    context.update(csrf(request))
    #prev_path=request.META['HTTP_REFERER']
    if request.method=='POST':
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            data = {'dat': username}
            return JsonResponse(data)
            #return redirect('main_page',number_page=1)
        else:
            data = {'dat': 'unknown user'}
            return JsonResponse(data)
    else:
        return render_to_response('registration/login.html',context)




def logout(request):
    auth.logout(request)
    return redirect('main_page',number_page=1)




def register2(request):
    context={}
    context.update(csrf(request))
    if request.method=="GET":
        return render_to_response('registration/register2.html',context)
    else:
        errors = {}
        flag=True
        allUsers=User.objects.all()

        username=request.POST.get('username','noUsername')
        email = request.POST.get('email', 'noEmail')
        password = request.POST.get('password', 'noPassword')
        password2 = request.POST.get('password2', 'noPassword2')
        check = allUsers.filter(username=username)
        reg=r'[a-z]'
        let=re.findall(reg,password,re.ASCII)
        let2 = re.findall(reg, password2, re.ASCII)
        errors['email'] = 'Correct'
        if check:
            errors['username']='Это имя пользователя уже занято'
            flag=False
        else:
            errors['username'] = 'Correct'

        if(password!=password2):
            errors['password2']='Пароли должны совпадать'
            flag = False
        elif(len(password2)<8)or(not let2)or(len(password2)>18):
            flag = False
            errors['password2'] = 'Пароль должен быть длиннее 8 и короче 19 символов, также должен содержать латинские буквы'
        else:
            errors['password2'] = 'Correct'

        if (len(password)<8)or(not let)or(len(password)>18):
            flag = False
            errors['password']='Пароль должен быть длиннее 8 и короче 19 символов, также должен содержать латинские буквы'
        else:
            errors['password'] = 'Correct'
        if(flag):
            newUser=User.objects.create_user(username=username,email=email,password=password)
            newUser.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)


        return JsonResponse(errors)



def add(request):
    context={}
    context.update(csrf(request))
    if request.method=='POST':
        name=request.POST.get('name','')
        category=request.POST.get('category','')
        if category=='Ноутбук':
            category='laptop'
        elif category=='Планшет':
            category='tablet'
        elif category=='Телефон':
            category='telephone'
        opisanie=request.POST.get('opisanie','')
        price=request.POST.get('price','')
        file=request.FILES.get('file','')
        user=auth.get_user(request)
        new_product=Product.objects.create(name=name,category=category,text=opisanie,price=price,image=file,saler=user)

        return redirect('main_page',number_page=1)
    else:
        return render(request,'add.html',context)

def my_products(request,number_page,pk):
    all_prod=Product.objects.all()
    user_id=auth.get_user(request).id
    my_prod=all_prod.filter(saler=user_id)

    q = request.GET.get('q')
    if pk==0:
        my_prod = all_prod.filter(saler=user_id)
    if pk == 1:
        my_prod = my_prod.filter(category='telephone')
    if pk == 2:
        my_prod = my_prod.filter(category='tablet')
    if pk == 3:
        my_prod = my_prod.filter(category='laptop')
    if q is not None:
        my_prod = my_prod.filter(name__icontains=q)
    curent_page=Paginator(my_prod,6)
    if int(number_page) > curent_page.num_pages:
        number_page = curent_page.num_pages
    my_prod = curent_page.page(number_page)
    context={'my_prod':my_prod,'filter':q,'pk':pk}
    return render(request,'my_products.html',context=context)


def edit(request,pk):
    product = Product.objects.get(pk=pk)
    image=product.image
    if request.method=='GET':
        return render(request,'edit.html',{'product':product})
    else:
        product.name=request.POST.get('name')
        product.category=request.POST.get('category')
        product.text=request.POST.get('opisanie')
        product.prise=request.POST.get('price')
        product.text=request.POST.get('opisanie')
        try_img=request.FILES.get('file','')
        if try_img!='':
            product.image=try_img
        product.save()
        return redirect('my_products',number_page=1,pk=0)

def my_delete(request,pk):
    all_prod=Product.objects.all()
    product=all_prod.get(pk=pk)
    product.delete()
    return redirect('my_products',number_page=1,pk=0)


def add_to_corz(request,id):
    all_products_in_korzina = korzina.objects.all()
    user = auth.get_user(request)
    data={'dat':''}
    if user.is_authenticated:
        product = Product.objects.get(id=id)
        check = all_products_in_korzina.filter(user=user.id, product=product.id)
        if not check:
            korz = korzina.objects.create(user=user, product=product)
            data['dat'] = id
            return JsonResponse(data)
        else:
            data['dat']='none'
            return JsonResponse(data)
    else:
        data['dat']='heh'
        return JsonResponse(data)

def Del(request,id):
    data={'dat':id}
    user_id = auth.get_user(request).id
    prod = korzina.objects.get(user=user_id, product=id)
    prod.delete()
    return JsonResponse(data)

def My_del(request,id):
    data={'dat':id}
    all_prod = Product.objects.all()
    product = all_prod.get(pk=id)
    product.delete()
    return JsonResponse(data)