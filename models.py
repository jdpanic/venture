from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class Person(models.Model):
 """
 Structure to represent all characters (players and NPCs) in the game.
 """
 name = models.CharField(max_length=50, unique=True)
 user = models.ForeignKey(User, null=True) # If it's null this person is an NPC
 alive = models.BooleanField(default=True) # alive on creation
 room = models.ForeignKey('Room', blank=True) # where am i?
 money = models.IntegerField(default=0) # in-game currency
 items = models.ManyToManyField('Item', blank=True)
 quests = models.ManyToManyField('Quest', blank=True) # Each person can be on many quests at once
 
 def __unicode__(self):
  return self.name

 def take(self, item):
  """
  Defines behavior for taking an item.
  Items can only be taken if they are in the same room as the player and
  if the player doesn't already have this item in their inventory. 
  """
  if item.room == self.room:
   self.items.add(item)
   # if not item.static:
   # item.visible = False # No one else can see or take this item
   # item.save()
    
   message = "You are now carrying " + item.name + ".\n"
   # Check all quests to see which ones have been completed etc.
   message += self._checkquests()
   
   return message
  
  else:
  # FLAG-DAN Consider returning a string stating that this item couldn't be taken
   # and possibly raising a flag to alert the admin of an error in the case that
   # the item isn't in this room (this implies that an item is visible when it shouldn't be)
   return "You can't carry that."
 
 def _checkquests(self):
  message = "" # String which will contain all of our quest-related messages
  for q in self.quests.all():
   itemcount = 0 # this will count up items in each quest below. It will be reset each iteration.
   for i in self.items.all():
    try:
     obj = q.items.objects.get(pk=i.id)
     itemcount += 1
     if itemcount >= q.items.count():
      message += "You've completed " + q.name + "!\n"
      self.quests.remove(q)
      break
    except:
     pass # what else should be done here?
     
  return message
 
 def spend(self, amount):
  """ Decreases the player's money. Makes sure it doesn't go under 0. """
  self.money -= amount
  if self.money < 0:
   self.money += amount
   return False # can't afford to pay
  
  return True
 
 def earn(self, amount):
  """ Increases player's money bo amount. Here for consistancy with spend. """
  self.money += amount
  return True
  
class Room(models.Model):
 """
 Defines room attributes.
 """
 description = models.TextField()  # Description of the room - visible to the player
 name = models.CharField(max_length=50, unique=True) # Room name
 exits = models.ManyToManyField('self', through='Exit', symmetrical=False, blank=True) #Exits from a room
 def __unicode__(self):
  return self.name
  
class Exit(models.Model): 
 """
 Exits and entrances available within each room.
 """
 from_room = models.ForeignKey(Room, related_name="exit")
 to_room = models.ForeignKey(Room, related_name="entrance")
 description = models.TextField() # Description of the path leading out from this exit
 locked = models.BooleanField(default=False)
 key_item = models.ForeignKey('Item', null=True, help_text="If locked is True, the player needs this item to get through the exit.", blank=True)
 
 #FLAG-DAN consider having a short name variable that we can replace 'door' with
 transition_message = models.TextField( blank=True, help_text="Descriptive message i.e. you step through the door.") 
 
 def __unicode__(self):
  return "from " + self.from_room.name + " to " + self.to_room.name

class Item(models.Model):
 """
 Defines item attributes.
 """
 #FLAG-DAN could we implement logic that allows some items to alter the player's attributes?
 # This would require modifying the player class - possibly adding some characteristics (hats?)
 name = models.CharField(max_length=50, unique=True) # Item name
 description = models.TextField(blank=True, null=True, help_text="Description as seen in person's inventory.")
 inroom_description = models.TextField(blank=True, null=True, help_text="Optional item description in a room e.g. you see a shiny jewel here.")
 room = models.ForeignKey(Room, help_text="Where can this item be found?")
 visible = models.BooleanField(default=True, help_text="Can this object be seen and taken?")
 def __unicode__(self):
  return self.name

class Quest(models.Model):
 """
 Defines quest behavior
 """
 name = models.CharField(max_length=50, unique=True)
 description = models.TextField()
 items = models.ManyToManyField(Item) # Items required to complete the quest
 time_limit = models.IntegerField(default=0, help_text="How long in seconds does player have to complete the quest? 0 = unlimited")
 cost = models.IntegerField(default=0) # how much does it cost to go on this quest?
 payout = models.IntegerField(default=0) # How much do you earn from completing the quest?
 def __unicode__(self):
  return self.name
  