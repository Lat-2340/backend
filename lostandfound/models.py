from datetime import datetime
from mongoengine import *

connect('items')

class Item(Document):
  user = StringField()
  item_name = StringField(max_length=70)
  is_lost = BooleanField(required=True)
  date_time = DateTimeField(default=datetime.now())
  features =StringField(max_length=150)
  description = StringField(max_length=150)
  pickup_address = StringField(max_length=70)
  match_info = ListField()

  def __str__(self):
    rep = 'user: {0}, item_name: {1}, is_lost: {2}, match_info: {3}'
    return rep.format(self.user, self.item_name, self.is_lost, self.match_info)

