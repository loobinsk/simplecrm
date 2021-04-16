import json
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Client, Call, CallComment, SelectedData
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def index(request):
	'''Главная страница'''
	all_call = Call.objects.all()
	managers_calls = Call.objects.filter(manager=request.user).order_by('-call_date').all()
	paginator = Paginator(all_call, 10)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
        # If page is not an integer deliver the first page
		posts = paginator.page(1)
	except EmptyPage:
        # If page is out of range deliver last page of results
		posts = paginator.page(paginator.num_pages)

	paginator_for_manager = Paginator(managers_calls, 10)
	try:
		managers_calls = paginator_for_manager.page(page)
	except PageNotAnInteger:
        # If page is not an integer deliver the first page
		managers_calls = paginator_for_manager.page(1)
	except EmptyPage:
        # If page is out of range deliver last page of results
		managers_calls = paginator_for_manager.page(paginator_for_manager.num_pages)

	template = 'homepage/homepage.html'
	context = {
		'page': page,
		'posts': posts,
		'all_call': all_call,
		'managers_calls': managers_calls,
	}

	return render(request, template, context)

@login_required
def clients(request):
	'''Вывод клиентов'''
	all_clients = Client.objects.order_by('-create_date').all()
	manager_clients = Client.objects.filter(curator=request.user).order_by('-create_date').all()
	all_clients1 = []
	managers_clients = []
	for i in all_clients:
		if i.full_name or i.email or i.current_situation or i.desired_situation or i.other_options or i.main_motive or i.proposed:
			all_clients1.append(i)
	for i in manager_clients:
		if i.full_name or i.email or i.current_situation or i.desired_situation or i.other_options or i.main_motive or i.proposed:
			managers_clients.append(i)

	all_clients3 = Paginator(all_clients1, 10)
	page = request.GET.get('page')
	try:
		all_clients = all_clients3.page(page)
	except PageNotAnInteger:
        # If page is not an integer deliver the first page
		all_clients = all_clients3.page(1)
	except EmptyPage:
        # If page is out of range deliver last page of results
		all_clients = all_clients3.page(all_clients3.num_pages)

	managers_clients1 = Paginator(managers_clients, 10)
	page = request.GET.get('page')
	try:
		managers_clients = managers_clients1.page(page)
	except PageNotAnInteger:
        # If page is not an integer deliver the first page
		managers_clients = managers_clients1.page(1)
	except EmptyPage:
        # If page is out of range deliver last page of results
		managers_clients = managers_clients1.page(managers_clients1.num_pages)

	template = 'clients/myclients.html'
	context = {'all_clients': all_clients, 'managers_clients': managers_clients,}
	return render(request, template, context)


@login_required
def client_list(request):
	'''Вывод потенциальных клиентов'''
	all_clients = Client.objects.order_by('-create_date').all()
	managers_clients = Client.objects.filter(curator=request.user).order_by('-create_date').all()

	all_clients1 = []
	managers_clients7 = []
	for i in all_clients:
		if not i.full_name and not i.email and not i.current_situation and not i.desired_situation and not i.other_options and not i.main_motive and not i.proposed:
			all_clients1.append(i)
	for i in managers_clients:
		if not i.full_name and not i.email and not i.current_situation and not i.desired_situation and not i.other_options and not i.main_motive and not i.proposed:
			managers_clients7.append(i)

	all_clients3 = Paginator(all_clients1, 10)
	page = request.GET.get('page')
	try:
		all_clients = all_clients3.page(page)
	except PageNotAnInteger:
        # If page is not an integer deliver the first page
		all_clients = all_clients3.page(1)
	except EmptyPage:
        # If page is out of range deliver last page of results
		all_clients = all_clients3.page(all_clients3.num_pages)

	managers_clients1 = Paginator(managers_clients7, 10)
	page = request.GET.get('page')
	try:
		managers_clients = managers_clients1.page(page)
	except PageNotAnInteger:
        # If page is not an integer deliver the first page
		managers_clients = managers_clients1.page(1)
	except EmptyPage:
        # If page is out of range deliver last page of results
		managers_clients = managers_clients1.page(managers_clients1.num_pages)

	template='clients/clients_list.html'
	context= {
		'all_clients': all_clients,
		'managers_clients': managers_clients,
	}
	return render(request, template, context)

@login_required
def client_detail(request, slug):
	'''Карточка клиента'''
	client123 = Client.objects.get(slug=slug)
	clients_calls = Call.objects.filter(client=client123)
	if request.method=='POST':
		if request.POST['comment']:
			comment = request.POST['comment']
			call_id = request.POST['call_for_comment']
			call = Call.objects.get(id=call_id)
			new_comment = CallComment(text=comment, author=request.user, call=call)
			new_comment.save()

		return HttpResponseRedirect(f'/client/{slug}/')
	template = 'clients/client_detail.html'
	context = {
		'client': client123,
		'clients_calls': clients_calls,
	}
	return render(request, template, context)

@login_required
def account(request):
	'''личный кабинет менеджера'''
	date_now = datetime.utcnow()
	date = date_now - timedelta(hours=12)
	last_call = Call.objects.filter(manager=request.user, call_date__range=[date, date_now])
	last_call_count = last_call.count()

	template = 'registration/account.html'

	context = {
		'last_call': last_call,
		'last_call_count': last_call_count,
	}
	return render(request, template, context)

@login_required
@csrf_exempt
def calendar(request):
	new_data = SelectedData()
	message=''
	if request.method=='POST':
		received_json_data=json.loads(request.body)
		for i in received_json_data.values():
			new_data = SelectedData(user=request.user.first_name, data1=i)
			if not SelectedData.objects.filter(data1=i, user=request.user.first_name).exists():
				new_data.save()
			else:
				get_data = SelectedData.objects.get(data1=i, user=request.user.first_name)
				if get_data.user == request.user.first_name:
					get_data.delete()

	template = 'registration/calendar.html'
	context = {'message': message}
	return render(request, template, context)

@login_required
def del_comment(request, comment_id, client_id):
	'''функция удаления комментария'''

	comment = CallComment.objects.get(id=comment_id)
	comment.delete()
	return HttpResponseRedirect(f'/client/{client_id}')

@login_required
def update_client(request, id):
	client = Client.objects.get(id=id)
	client_full_name = request.POST['full_name']
	client_email = request.POST['email']
	client_source = request.POST['source_call']
	client_current_situation = request.POST['current_situation']
	client_desired_situation = request.POST['desired_situation']
	client_other_options = request.POST['other_option']
	client_main_motive = request.POST['main_motive']
	client_proposed = request.POST['proposed']
	slug = client.slug

	client.full_name = client_full_name
	client.email = client_email
	client.call_source = client_source
	client.current_situation = client_current_situation
	client.desired_situation =client_desired_situation
	client.other_options = client_other_options
	client.main_motive = client_main_motive
	client.proposed = client_proposed
	print(client.call_source)
	client.save()
	print(client.full_name, client.email, client.call_source)
	return HttpResponseRedirect(f'/client/{slug}/')

@login_required
def update_user(request):
	user = User.objects.get(username=request.user.username)
	user.first_name = str(request.POST['username'])
	user.save()
	return HttpResponseRedirect(f'/account/')

@login_required
def update_pass(request):
	form = PasswordChangeForm(user=request.user, data=request.POST or None)
	if form.is_valid():
		form.save()
		update_session_auth_hash(request, form.user)
		return redirect('sucs_change')

	template = 'registration/changepsw.html'
	context = {'form': form}
	return render(request, template, context)

@login_required
def sucsch(request):
	return render(request, 'registration/sucs_chps.html')


def new_client(request):
	template = 'clients/add_new_client.html'
	if request.method == 'POST':
		client_phone_number = request.POST['phone_number']
		if '+7' in client_phone_number:
			client_phone_number = client_phone_number.replace("+7","")
		client_full_name = request.POST['full_name']
		client_email = request.POST['email']
		client_source = request.POST['source_call']
		client_current_situation = request.POST['current_situation']
		client_desired_situation = request.POST['desired_situation']
		client_other_options = request.POST['other_option']
		client_main_motive = request.POST['main_motive']
		client_proposed = request.POST['proposed']
		client_curator = request.user
		new_client = Client(
			curator=client_curator, 
			full_name=client_full_name, 
			phone=client_phone_number,
			email= client_email,
			call_source=client_source, 
			current_situation = client_current_situation,
			desired_situation = client_desired_situation,
			other_options = client_other_options,
			main_motive = client_main_motive,
			proposed = client_proposed,
			)
		new_client.save()
		return HttpResponseRedirect('/clients/')
	context = {}
	return render(request, template, context)