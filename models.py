from django.db import models

class Person(models.Model):
 """ This model represents all characters (players and NPCs) in the game. """
 name = models.CharField(max_length=50, unique=True)
 alive = models.BooleanField(default=True) # alive on creation
 room = models.ForeignKey('Room') # where am i?
 #items = models.ForeignKey('Item', related_name='owner')
 # score = models.IntegerField(blank=True)
 def __unicode__(self):
  return self.name

 def take(self, what): # take an item
  #what.room = None # it belongs to this person now
  if what.room == self.room and what.takeable:
   what.owner = self
   return True
  else:
   return False

class Room(models.Model):
 description = models.TextField()  # You are in the drawing room. Burning fires are everywhere.
 name = models.CharField(max_length=50, unique=True) # Drawing Room
 exits = models.ManyToManyField('self', through='Exit', symmetrical=False)
 def __unicode__(self):
  return self.name
  
class Exit(models.Model): 
 from_room = models.ForeignKey(Room, related_name="exit")
 to_room = models.ForeignKey(Room, related_name="entrance")
 description = models.TextField() # A spiral staircase leads to _
 opened = models.BooleanField(default=True, help_text="Is this exit opened or closed?")
 transition_message = models.TextField( blank=True, help_text="You step through the door.")
 def __unicode__(self):
  return "from " + self.from_room + " to " + self.to_room

class Item(models.Model):
 name = models.CharField(max_length=50, unique=True) # Chrystal Ball
 description = models.TextField(blank=True, null=True, help_text="Description as seen in person's inventory.")
 inroom_description = models.TextField(blank=True, null=True, help_text="Optional item description in a room e.g. you see a shiny jewel here.")
 room = models.ForeignKey(Room, help_text="Where can this item be found?")
 owner = models.ForeignKey(Person, blank=True, null=True, help_text="Leave this blank.")
 takeable = models.BooleanField(default=True, help_text="Can this object be taken?") # can this item be moved?
 def __unicode__(self):
  return self.name
 def used_on(self, other_item): # this is the victim method - what does this object do when something's used on it?
  pass
 def use(self, what=None): # What am I using this object on?
  pass

