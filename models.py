from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class Person(models.Model):
 """ This model represents all characters (players and NPCs) in the game. """
 name = models.CharField(max_length=50, unique=True)
 user = models.ForeignKey(User, null=True) # If it's null this person is an NPC
 alive = models.BooleanField(default=True) # alive on creation
 room = models.ForeignKey('Room') # where am i?
 money = models.IntegerField(default=0) # in-game currency
 items = models.ManyToManyField('Item')
 quests = models.ManyToManyField('Quest') # Each person can be on many quests at once
 def __unicode__(self):
  return self.name

 def take(self, what): # take an item
  if what.room == self.room and self.items.objects.get(pk=what.id) is None:
   self.items.add(what)
   if not what.static:
    what.visible = False # No one else can see or take this item
   # check to see if this item is in any quests.
   for q in self.quests:
    try:
     obj = q.items.objects.get(pk=what.id)
     
    except:
     pass
    
   return "You are now carrying " + what.name
  else:
   return None

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
 locked = models.BooleanField(default=False)
 key_item = models.ForeignKey('Item', help_text="If locked is True, the player needs this item to get through the exit.")
 transition_message = models.TextField( blank=True, help_text="You step through the door.")
 def __unicode__(self):
  return "from " + self.from_room + " to " + self.to_room

class Item(models.Model):
 name = models.CharField(max_length=50, unique=True) # Chrystal Ball
 description = models.TextField(blank=True, null=True, help_text="Description as seen in person's inventory.")
 inroom_description = models.TextField(blank=True, null=True, help_text="Optional item description in a room e.g. you see a shiny jewel here.")
 room = models.ForeignKey(Room, help_text="Where can this item be found?")
 visible = models.BooleanField(default=True, help_text="Can this object be seen and taken?")
 def __unicode__(self):
  return self.name

class Quest(models.Model):
 name = models.CharField(max_length=50, unique=True)
 description = models.TextField()
 items = models.ManyToManyField(Item)
 time_limit = models.IntegerField(default=0, help_text="How long in seconds does player have to complete the quest? 0 = unlimited")
 cost = models.IntegerField(default=0) # how much does it cost to go on this quest?
 payout = models.IntegerField(default=0) # How much do you earn from completing the quest?
 def __unicode__(self):
  return self.name
  
