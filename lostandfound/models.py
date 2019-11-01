from django.db import models

from users.models import CustomUser, PickupLocation

class Item(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  feature_color = models.CharField(max_length=15)
  feature_size = models.CharField(max_length=15)
  feature_category = models.CharField(max_length=15)
  date = models.DateField(auto_now_add=True)
  location_lat = models.DecimalField(blank=False, max_digits=19, decimal_places=10)
  location_long = models.DecimalField(blank=False, max_digits=19, decimal_places=10)
  description = models.CharField(max_length=150, null=True, blank=True)

  def __str__(self):
    rep = 'user: {0}, color: {1}, size: {2}, category: {3}, description: {4}'
    return rep.format(self.user, self.feature_color, self.feature_size, self.feature_category, self.description)

class FoundItem(Item):
  image = models.ImageField(null=True, blank=True)
  pickup_address = models.ForeignKey(PickupLocation, null=True, on_delete=models.SET_NULL)

  def __str__(self):
    super_rep = super().__str__()
    return '{0}, pickup: {1}'.format(super_rep, self.pickup_address)
