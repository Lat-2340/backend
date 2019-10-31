from datetime import datetime
from mongoengine import *

connect('item')

class Item(Document):
  user = StringField()
  features = ListField(required=True)
  date_time = DateTimeField(default=datetime.now())
  location = GeoPointField()
  description = StringField(max_length=150)

  meta = {
    'allow_inheritance': True
  }

  def __str__(self):
    rep = 'user: {0}, features: {1}, location: {2}, date_time: {3}, description: {4}'
    return rep.format(self.user, self.features, self.location, self.date_time, self.description)

class FoundItem(Item):
  image = ImageField()
  pickup_address = StringField(max_length=70, required=True)

  def __str__(self):
    rep = 'user: {0}, features: {1}, location: {2}, pickup: {3}, date_time: {4}, description: {5}'
    return rep.format(self.user, self.features, self.location, self.pickup_address, self.date_time,  self.description)
