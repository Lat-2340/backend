from djongo import models

class GeoLocation(models.Model):
  latitude = models.DecimalField(max_digits=22, decimal_places=16)
  longitude = models.DecimalField(max_digits=22, decimal_places=16)

  class Meta:
    abstract = True # never use this model as a standalone model

  def __str__(self):
    return 'lat: {0}, long: {1}'.format(self.latitude, self.longitude)

# shortened version of users.models.Office
class PickupLocation(models.Model):
  address = models.CharField(max_length=70, primary_key=True)
  office = models.CharField(max_length=30)

  class Meta:
    app_label = 'lostandfound'

  def __str__(self):
    rep = "office: {0}, org: {1}, address: {2}"
    return rep.format(self.office, self.address)

class Item(models.Model):
  # TODO: complete categories
  CATEGORIES = (
    ('BAGS', 'BAGS'),
    ('SUITCASES', 'SUITCASES'),
    ('BOOKS', 'BOOKS'),
    ('PHONES', 'CELL PHONES'),
    ('ELECTRONICS', 'ELECTRONICS & ACCESSORIES'),
    ('CLOTHING', 'CLOTHING & ACCESSORIES'),
    ('JEWELRY', 'JEWELRY'),
    ('MUSIC INSTRUMENTS', 'MUSIC INSTRUMENTS')
  )

  category = models.CharField(choices=CATEGORIES, max_length=30)
  date_time = models.DateTimeField()
  location = models.EmbeddedModelField(
    model_container=GeoLocation,
  )
  features = models.TextField(max_length=150)

  objects = models.DjongoManager()

  def __str__(self):
    rep = 'category: {0}, loc: {1}, features: {2}'
    return rep.format(self.category, self.location, self.features)

  class Meta:
    abstract = True

class LostItem(Item):
  class Meta:
    app_label = 'lostandfound'

class FoundItem(Item):
  image = models.ImageField()
  pickup_location = models.ForeignKey(PickupLocation, on_delete=models.CASCADE)
  class Meta:
    app_label = 'lostandfound'

class LostandfoundRouter(object):
  '''A router to control all database operations on models in the lostandfound application'''

  def db_for_read(self, model, **hints):
    if model._meta.app_label == 'lostandfound':
      return 'mongo'
    return None

  def db_for_write(self, model, **hints):
    if model._meta.app_label == 'lostandfound':
      return 'mongo'
    return None

  def allow_relation(self, obj1, obj2, **hints):
    if obj1._meta.app_label == 'lostandfound' or obj2._meta.app_label == 'lostandfound':
      return True
    return None

  def allow_syncdb(self, db, model):
    if db == 'mongo':
      return model._meta.app_label == 'lostandfound'
    elif model._meta.app_label == 'lostandfound':
      return False
    return None