# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from venture.models import Item, Room, Person, Exit
from django.template import RequestContext
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

def login(request):
 u = auth.authenticate(request.POST['username'], request.POST['pwd'])
 if u:
  if u.is_active:
   auth.login(request, u)
   return render_to_response('venture/choose.html')
  else:
   return render_to_response('venture/banned.html')
 else:
  messages.warning(request, "The username/password combination  is invalid.")
  return HttpResponseRedirect(reverse('venture.views.main'))

@login_required
def choose(request):
 if request.POST:
  if request.POST['pid']:
   me = Person.objects.get(pk=request.POST['pid'])
  elif request.POST['name']: # if there's no pid or if that pid is invalid we try and create someone
   me = Person()
   me.name = request.POST['name']
   me.room = Room.objects.get(name='Home Room') # ghetto
   me.user = request.user
   me.save()
  
  me.alive = True
  request.session['p_id'] = me.id
  request.session.set_expiry(0) # expires when the browser closes
  return HttpResponseRedirect(reverse('venture.views.game'))
 
 return render_to_response("venture/choose.html")
 
@login_required
def game(request):
 try:
  me = Person.objects.get(pk=request.session['p_id'])
 except  Person.DoesNotExist: # this should not be happening. Where should they go?
  return HttpResponseRedirect(reverse('venture.views.main'))

 return render_to_response('venture/game.html', {'me': me}, context_instance=RequestContext(request))

@login_required
def action(request):
 me = Person.objects.get(pk=request.session['p_id'])
 act = request.POST['do_what']
 if act=="take":
  obj = get_object_or_404(Item.objects, pk=request.POST['on_what'])
  if me.take(obj):
   messages.success(request, "You are now carrying " + obj.name)
  else:
   messages.warning(request, "You can't carry " + obj.name)
 elif act=="go":
  obj = get_object_or_404(Exit.objects, pk=request.POST['on_what'])
  if not obj.locked:
   me.room = obj.to_room
   me.save()
   messages.success(request, obj.transition_message)
  else:
   messages.warning(request, "LOCKED")
 elif act == "quest":
  q = get_object_or_404(Quest.objects, pk=request.post["on_what"])
  if q not in me.quests:
   me.quests.add(q)
   messages.success(request, q.description)
 
 return HttpResponseRedirect(reverse('venture.views.game'))

def main(request):
 return render_to_response("venture/login.html", context_instance=RequestContext(request))
 
def quit(request):
 me = Person.objects.get(pk=request.session['p_id'])
 me.alive = False
 me.save()
 request.session['p_id'] = '0'
 auth.logout(request, me.user)
 return render_to_response("venture/quit.html")
 