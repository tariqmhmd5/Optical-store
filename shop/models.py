from django.db import models

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    category = models.CharField(max_length=50,default="",choices=(('Men Eyewear','Men Eyewear'),('Women Eyewear','Women Eyewear')))
    price = models.IntegerField(default=0)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='products/images',default="")

    def __str__(self):
        return self.product_name
    