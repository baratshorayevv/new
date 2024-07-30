from datetime import datetime

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(default='', blank=True)
    image = models.ImageField(upload_to='uploads/product/')
    is_sale = models.BooleanField(default=False)
    the_sale_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name}. {self.last_name}'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=50)
    date = models.DateField(default=datetime.now)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.customer}. {self.product}. {self.quantity}'



from .bad_words import BAD_WORDS

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        for word in BAD_WORDS:
            if word in self.content.lower():
                raise ValidationError('Comment contains inappropriate language.')

    def save(self, *args, **kwargs):
        self.clean()
        super(Comment, self).save(*args, **kwargs)




@receiver(pre_save, sender=Comment)
def check_bad_words(sender, instance, **kwargs):
    for word in BAD_WORDS:
        if word in instance.content.lower():
            instance.user.is_active = False
            instance.user.save()
            raise ValidationError("Your comment contains inappropriate language, and your account has been deactivated.")
