# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from venture.models import Item, Room, Person, Exit, Quest
from venture.forms import PersonForm
from django.template import RequestContext
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

def login(request):
 if request.POST:
  u = auth.authenticate(username=request.POST['username'], password=request.POST['pwd'])
  if u:
   if u.is_active:
    auth.login(request, u)
    return render_to_response('venture/choose.html', context_instance=RequestContext(request))
   else:
    return render_to_response('venture/banned.html')
  else:
   messages.warning(request, "The username/password combination is invalid.")
   return HttpResponseRedirect(reverse('venture.views.login'))
 
 return render_to_response('venture/login.html', context_instance=RequestContext(request))

@login_required
def new_person(request):
 title = "Create a New Character"
 if request.POST:
  form = PersonForm(request.POST)
  if form.is_valid():
   me = form.save()
   me.room = Room.objects.get(pk=1)
   me.user = request.user
   me.save()
   request.session['p_id'] = me.id
   request.session.set_expiry(0) # expires when the browser closes
   return render_to_response('venture/game.html', {'me': me}, context_instance=RequestContext(request))
  else:
   return render_to_response('venture/form.html', {'title': title, 'form': form}, context_instance=RequestContext(request))

 form = PersonForm()
 return render_to_response('venture/form.html', {'title': title, 'form': form}, context_instance=RequestContext(request))

def choose(request, pid=None):
 if pid:
  try:
   me = Person.objects.get(pk=pid)
  except Person.DoesNotExist:
   return render_to_response('venture/choose.html', context_instance=RequestContext(request))

  request.session['p_id'] = me.id
  return render_to_response('venture/game.html', {'me': me}, context_instance=RequestContext(request))
 else:
  return render_to_response('venture/choose.html', context_instance=RequestContext(request))

@login_required
def game(request):
 try:
  me = Person.objects.get(pk=request.session['p_id'])
 except  Person.DoesNotExist: # this should not be happening. Where should they go?
  return HttpResponseRedirect(reverse('venture.views.main'))

 return render_to_response('venture/game.html', {'me': me}, context_instance=RequestContext(request))

@login_required
def quests(request):
 return render_to_response("venture/quests.html", {'quests': Quest.objects.all()}, context_instance=RequestContext(request))

@login_required
def action(request):
 me = Person.objects.get(pk=request.session['p_id'])
 act = request.POST['do_what']
 if act=="take":
  obj = get_object_or_404(Item.objects, pk=request.POST['on_what'])
  messages.success(request, me.take(obj))
 elif act=="go":
  obj = get_object_or_404(Exit.objects, pk=request.POST['on_what'])
  if not obj.locked:
   me.room = obj.to_room
   me.save()
   messages.success(request, obj.transition_message)
  else:
   messages.warning(request, "LOCKED")
 elif act == "quest":
  q = get_object_or_404(Quest.objects, pk=request.POST["on_what"])
  if me.spend(q.cost):
   me.quests.add(q)
   me.save()
   messages.success(request, q.description)
  else:
   messages.warning(request, "You can't afford that quest.")
 elif act == "use":
  exits = Exit.objects.filter(from_room=me.room)
  it = Item.objects.get(pk=request.POST['on_what'])
  for ex in exits:
   if ex.locked and ex.key_item == it:
    messages.success(request, ex.unlock_message)
    ex.locked = False
    ex.save() # Just in case

 return HttpResponseRedirect(reverse('venture.views.game'))

def main(request):
 return render_to_response("venture/login.html", context_instance=RequestContext(request))
 
def quit(request):
 request.session['p_id'] = '0'
 return HttpResponseRedirect(reverse('venture.views.choose'))
 
def logout(request):
 auth.logout(request)
 return HttpResponseRedirect(reverse('venture.views.login'))
 
def reset(request):
 exits = Exit.objects.all()
 fake = Item.objects.get(name="Fake Item")
 for ex in exits:
  if ex.key_item != fake:
   ex.locked = True
   ex.save()

 return HttpResponseRedirect(reverse('venture.views.main'))

