from datetime import datetime
from mongoengine import *

connect('items')

class Item(Document):
  user = StringField()
  is_lost = BooleanField(required=True)
  date_time = DateTimeField(default=datetime.now())
  location = GeoPointField()
  features =DictField()
  description = StringField(max_length=150)
  pickup_address = StringField(max_length=70)

  def __str__(self):
    rep = 'user: {0}, is_lost: {1}, date_time: {2}, features: {3}, description: {4}'
    return rep.format(self.user, self.is_lost, self.location, self.features, self.description)

