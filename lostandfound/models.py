from datetime import datetime
from mongoengine import *

connect('item')

class Item(Document):
  # TODO: complete categories
  CATEGORIES = ('cat1', 'cat2')

  category = StringField(choices=CATEGORIES, max_length=30, required=True)
  date_time = DateTimeField(default=datetime.now())
  location = GeoPointField()
  description = StringField(max_length=150)

  meta = {
    'allow_inheritance': True
  }

  def __str__(self):
    rep = 'category: {0}, location: {1}, date_time: {2}, description: {3}'
    return rep.format(self.category, self.location, self.date_time, self.description)

class FoundItem(Item):
  image = ImageField()
  pickup_address = StringField(max_length=70)

  def __str__(self):
    rep = 'category: {0}, location: {1}, pickup: {2}, date_time: {3}, description: {4}'
    return rep.format(self.category, self.location, self.pickup_address, self.date_time,  self.description)
