from django.db import models
from shopease_user.models import User
from product.models import Product

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    added_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('user','product') #to prevent the duplicate wishlist items

    def __str__(self):
        return f"{self.user}-{self.product}"
