from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from counter.models import *
from counter.forms import *
# Create your views here.
def index(request):
	return render(request,'counter/index.html')

def totalScore(request):
	wins = Result.objects.filter(won=True).count()
	losses = Result.objects.filter(won=False).count()
	return render(request,'counter/total.html',{'wins':wins,'losses':losses})

def scoreWith(request):
	if request.method == "GET":
		return render(request, 'counter/scoreWith.html', {'form':IncludeExcludeForm})
	form = IncludeExcludeForm(request.POST)
	if form.is_valid():
		players = list(form.cleaned_data['player_choices'])
		maps = list(form.cleaned_data['map_choices'])
		p_inc = form.cleaned_data['player_select']
		m_inc = form.cleaned_data['map_select']

		if m_inc == "include":
			if p_inc == "include":
				filtered = Result.objects.filter(map_played__in=maps)
				for player in players:
					filtered = filtered.filter(played_with__in=[player])
			else:
				filtered = Result.objects.filter(map_played__in=maps)
				for player in players:
					filtered = filtered.exclude(played_with__in=[player])
		else:
			if p_inc == "include":
				filtered = Result.objects.exclude(map_played__in=maps)
				for player in players:
					filtered = filtered.filter(played_with__in=[player])
			else:
				filtered = Result.objects.exclude(map_played__in=maps)
				for player in players:
					filtered = filtered.exclude(played_with__in=[player])
		wins = filtered.filter(won=True).count()
		losses = filtered.filter(won=False).count()
		formatted = []
		for item in filtered:
			players_list = []
			for player in item.played_with.all():
				players_list.append(str(player))
			formatted.append((item.won,str(item.map_played),item.date,players_list,item.comments))
		return render(request, 'counter/withmatchhistory.html', {'history':formatted,'wins':wins,'losses':losses,'m_inc':m_inc=="include",'p_inc':p_inc=='include','players':players,'maps':maps})
	
	else:
		return render(request, 'counter/scoreWith.html', {'form':IncludeExcludeForm})

def report(request):
	if request.method == "GET":
		return render(request, 'counter/report.html', {'form':AddForm,'success':False})
	form = AddForm(request.POST)
	try:
		form.save()
	except:
		return render(request, 'counter/report.html', {'form':form,'success':False})
	return HttpResponseRedirect('/matchhistory/')

def addplayer(request):
	if request.method == "GET":
		return render(request, 'counter/addplayer.html', {'form':AddPlayerForm,'success':False})
	form = AddPlayerForm(request.POST)
	try:
		form.save()
	except:
		return render(request, 'counter/addplayer.html', {'form':AddPlayerForm,'success':False})
	return render(request, 'counter/addplayer.html', {'success':True})

def winratevstime(request):
	results = Result.objects.all().order_by('date')
	winrate = []
	wins = 0
	games = 0
	for item in results:
		games += 1
		if item.won:
			wins += 1
		playwith = item.played_with.all()
		players = []
		for p in playwith:
			players.append(str(p))
		rate = wins/games
		brightest = 200
		if rate < .4:
			r = brightest
			g = 0
			b = 0
		elif rate < .5:
			r = brightest
			g = int((rate-.4)*brightest*10)
			b = 0
		elif rate < .6:
			r = int(brightest - (rate-.5)*brightest*10)
			g = brightest
			b = 0
		else:
			r = 0
			g = brightest
			b = 0

		winrate.append((wins/games,item.date,players,r,g,b))
	return render(request, 'counter/winratevstime.html', {'winrate':winrate})

def matchhistory(request):
	results = Result.objects.all()
	formatted = []
	for item in results:
		players = []
		for player in item.played_with.all():
			players.append(str(player))
		formatted.append((item.won,str(item.map_played),item.date,players,item.comments))
	wins=Result.objects.filter(won=True).count()
	losses=Result.objects.filter(won=False).count()
	return render(request, 'counter/matchhistory.html', {'history':formatted,'wins':wins,'losses':losses})