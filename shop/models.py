from django.db import models
from accounts.models import Company
from django.db.models.signals import pre_save
from django.utils.text import slugify
# Create your models here.


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

    def __str__(self):
        return self.name


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_product_receiver, sender=Product)
