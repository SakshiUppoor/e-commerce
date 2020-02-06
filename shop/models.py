from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from .utils import holiday
import datetime


class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    profile_images = models.ImageField(
        default="profile_images/default.jpg", upload_to='profile_images', blank=True, null=True)
    country = models.CharField(max_length=1000, blank=True)
    facebook = models.CharField(max_length=1000, blank=True)
    twitter = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        if self.is_company:
            return self.first_name
        elif self.is_customer:
            return self.first_name+" "+self.last_name
        else:
            return self.username


class Company(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="company")
    description = models.CharField(max_length=255, blank=True, null=True)
    header = models.ImageField(
        default="headers/default.jpg", upload_to='headers', blank=True, null=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = "companies"


@receiver(post_save, sender=User)
def create_components(sender, **kwargs):
    if kwargs['created'] and kwargs.get('instance').is_company == True:
        company = Company.objects.create(user=kwargs.get('instance'))
    elif kwargs['created'] and kwargs.get('instance').is_customer == True:
        cart = Cart.objects.create(user=kwargs.get('instance'))
    if kwargs['created']:
        list = holiday.get_holidays(kwargs.get('instance').country)["holidays"]
        for l in list:
            new_c, created = Campaign.objects.get_or_create(uuid=l["uuid"])
            if created == True:
                date = l["date"].replace('2019', '2020')
                new_c.name = l["name"]
                new_c.date = date
                new_c.country = l["country"]
                new_c.discount = 10
            new_c.save()


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "subcategories"


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    rate = models.FloatField(default=0)
    description = models.CharField(max_length=1000, blank=True)
    in_stock = models.IntegerField(default=0)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True)
    product_image = models.ImageField(
        default="product_images/default.jpg", upload_to='product_images', blank=True, null=True)
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, null=True)
    discount = models.FloatField(default=0.0)
    discounted_rate = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Product)
def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="cart")

    def __str__(self):
        return self.user.first_name + "'s Cart"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cost = models.FloatField(default=0)
    is_saved_for_later = models.BooleanField(default=False)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True)


class WishlistItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wishlistitem")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + self.product.name


'''
@receiver(post_save, sender=OrderItem)
def update_order_item_cost(sender, instance, **kwargs):
    instance.order_item_cost = instance.product.rate * instance.quantity

'''


class Order(models.Model):
    total = models.FloatField(default=0)
    address1 = models.CharField(max_length=1000, blank=True)
    address2 = models.CharField(max_length=1000, blank=True)
    city = models.CharField(max_length=1000, blank=True)
    country = models.CharField(max_length=1000, blank=True)
    zip = models.CharField(max_length=6, blank=True)
    phone = models.CharField(max_length=1000, blank=True)
    first_name = models.CharField(max_length=1000, blank=True)
    last_name = models.CharField(max_length=1000, blank=True)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_item_cost = models.FloatField(default=0)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True)


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review")
    rating = models.FloatField(default=0.0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=1000, blank=True)


@receiver(post_save, sender=Review)
def post_save_rating_receiver(sender, instance, *args, **kwargs):
    product = kwargs.get('instance').product
    reviews = Review.objects.filter(product=product)
    count = 0
    rating_sum = 0
    for review in reviews:
        rating_sum += review.rating
        count += 1
    product.rating = rating_sum/count


class Campaign(models.Model):
    name = models.CharField(max_length=100, blank=True)
    uuid = models.CharField(max_length=100, blank=True)
    date = models.DateField(default=datetime.date.today)
    discount = models.FloatField(default=0.0)
    country = models.CharField(max_length=1000, blank=True)

    def activate(self):
        products = Product.objects.all()
        for product in products:
            product.discount = self.discount
            product.discounted_rate = (100-self.discount)/100 * product.rate
            product.save()
        return

    def __str__(self):
        return self.name
