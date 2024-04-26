from django.contrib import admin
from django.urls import path,include
from .import views as v
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('add-category', v.AddCategory.as_view(),name="post"),
    path('add-admin', v.AddAdmin.as_view(),name="post"),
    path('add-product', v.AddProduct.as_view(),name="post"),
    path('update-product', v.UpdateProduct.as_view(),name="post"),
    path('delete-product', v.DeleteProduct.as_view(),name="post"),
    path('', v.index,name="index"),
]
