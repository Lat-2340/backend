from datetime import datetime
from mongoengine import *

connect('items')

class Item(Document):
  user = StringField()
  is_lost = BooleanField(required=True)
  date_time = DateTimeField(default=datetime.now())
  location = GeoPointField()
  features =StringField(max_length=150)
  description = StringField(max_length=150)
  pickup_address = StringField(max_length=70)
  matched_imgs = ListField()

  def __str__(self):
    rep = 'user: {0}, is_lost: {1}, matched_imgs: {2}'
    return rep.format(self.user, self.is_lost, self.matched_imgs)

