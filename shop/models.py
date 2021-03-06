from django.db import models
from django.contrib.auth.models import User
    

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    category = models.CharField(max_length=50,default="",choices=(('Men Eyewear','Men Eyewear'),('Women Eyewear','Women Eyewear')))
    price = models.IntegerField(default=0)
    pub_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='products/images',default="")

    def __str__(self):
        return self.product_name


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    def __str__(self):
        return self.product.product_name
    

class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)   
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=100,null=True)
    phone = models.IntegerField(null=True)
    address = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    zipcode = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.address
    
    