from django.shortcuts import render,redirect
from .jwt1 import adminJWTAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import *
from .serializers import *

from rest_framework.permissions import IsAuthenticated
# Create your views here.


class AddCategory(GenericAPIView):
    authentication_classes=[adminJWTAuthentication,]
    permission_classes=[IsAuthenticated]

    def post(self,request):
        data=request.data
        categoryserializer = CategorySerializer(data=data)
        if categoryserializer.is_valid():
            categoryserializer.save()

            response_={
                'status':1,
                'msg':'Category Created Successfully.',
                'data':{}
            }
            return Response(response_,status=200)
        else:
            response_={
                'status':0,
                'msg':'Category Not Created.',
                'data':{}
            }
            return Response(response_,status=400)




class AddProduct(GenericAPIView):
    authentication_classes=[adminJWTAuthentication,]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        data=request.data
        data['created_at'] = timezone.now()
        categoryserializer = ProductSerializer(data=data)
        if categoryserializer.is_valid():
            categoryserializer.save()

            response_={
                'status':1,
                'msg':'Product Created Successfully.',
                'data':{}
            }
            return Response(response_,status=200)
        else:
            response_={
                'status':0,
                'msg':'Product Not Created.',
                'data':{}
            }
            return Response(response_,status=400)
        
    def get(self,request):
        authentication_classes=[adminJWTAuthentication,]
        permission_classes=[IsAuthenticated]

        productobj = Product.objects.filter(status=True)
        productserializer = ProductSerializer(productobj,many=True)
        if productserializer.data !=[]:
            response_={
                    'status':1,
                    'msg':'Product List Found Successfully.',
                    'data':productserializer.data
                }
            return Response(response_,status=200)
        else:
            response_={
                    'status':0,
                    'msg':'No product Data Found.',
                    'data':productserializer.data
                }
            return Response(response_,status=404)
        


class UpdateProduct(GenericAPIView):
    authentication_classes=[adminJWTAuthentication,]
    permission_classes=[IsAuthenticated]

    def post(self,request):
        data=request.data
        productobj=Product.objects.filter(id=data['id']).first()
        data['updated_at'] = timezone.now()
        categoryserializer = ProductSerializer(productobj,data=data)
        if categoryserializer.is_valid():
            categoryserializer.save()

            response_={
                'status':1,
                'msg':'Product Updated Successfully.',
                'data':{}
            }
            return Response(response_,status=200)
        else:
            response_={
                'status':0,
                'msg':'Product Not Updated.',
                'data':{}
            }
            return Response(response_,status=400)
        
    
class DeleteProduct(GenericAPIView):
    authentication_classes=[adminJWTAuthentication,]
    permission_classes=[IsAuthenticated]

    def post(self,request):
        id = request.data.get('id')
        if id is not None and id !="":
            productobj = Product.objects.filter(id=id).first()
            if productobj is not None:
                productobj.status = False
                productobj.save()
                response_={
                    'status':1,
                    'msg':'Product Deleted Successfully.',
                    'data':{}
                }
                return Response(response_,status=200)
            else:
                response_={
                    'status':0,
                    'msg':'Product Not Found.',
                    'data':{}
                }
                return Response(response_,status=200)
        else:
            response_={
                'status':0,
                'msg':'ID is required.',
                'data':{}
            }
            return Response(response_,status=200)
        


class AddAdmin(GenericAPIView):

    def post(self,request):
        data=request.data
        serializer=AdminSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            adminobj = Admin.objects.filter(email=serializer.data['email']).first()
            admintokenobj = adminToken.objects.create(admin=serializer.data['id'],authToken=adminobj.token)

            response_={
                    'status':1,
                    'msg':'User Created Successfully.',
                    'data':{}
            }
            return Response(response_,status=200)
        else:
            print("error",serializer.errors)


import random
import string
from django.utils import timezone
import celery
from celery import shared_task
@shared_task
def index(request):
    if request.method == "POST":
        count = request.POST.get('productcount')
        print("count",count)
        for i in range(0,int(count)):
            print("i",i)
            catobj = Category.objects.filter().first()
            category_id = catobj.id
            title = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=10))
            description = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=100))
            price = random.randint(40,100) 
            status = True
            created_at = timezone.now()
            Product.objects.create(category_id=category_id,title=title,description=description,price=price,status=status,created_at=created_at)
            
        return redirect('ProductMaster:index')
    prodobj=Product.objects.filter()
    prodser = ProductSerializer(prodobj,many=True)
    return render(request,'index.html',{'productlist':prodser.data})



    
    