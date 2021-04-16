from core.models import Client, Call, CallComment, SelectedData
from django.http import HttpResponse
from core.sqlighter import SQLighter
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime


def parse(request):
	parse_db = SQLighter(2640)
	data_list = parse_db.get_data()
	black_list = ['2003', '101', '2200100', '104', '89157973467','89637683005'] #3467 екатерина, 3005 павел
	for i in data_list:
			if str(i['исходящий номер']) not in black_list and str(i['входящий номер']) not in black_list:
				if str(i['статус звонка']) == 'ANSWERED':
					
					if not User.objects.filter(username=i['входящий номер']).exists():
							new_user = User.objects.create_user(username=i['входящий номер'], password='pass123')
							new_user.save()

					if not Client.objects.filter(phone=i['исходящий номер']).exists():
						curator = orderly_manager_by_string_datetime(i['время поступления звонка'])
						new_client = Client(phone=i['исходящий номер'], curator=curator)
						new_client.save()
					if not Call.objects.filter(call_date=i['время поступления звонка']).exists():
						
						manager = orderly_manager_by_string_datetime(i['время поступления звонка'])
						
						new_call = Call(
							client= Client.objects.get(phone=str(i['исходящий номер'])), 
							manager=manager, 
							call_status=0, url=i['путь к файлу'],
							call_date=i['время поступления звонка'],
							)
						new_call.save()
	return HttpResponse('идет парсинг')

def orderly_manager_by_string_datetime(datetime):
	call_datetime = parse_datetime(datetime)
	if SelectedData.objects.filter(data1=call_datetime.date()).exists():
		selected_data = SelectedData.objects.get(data1=call_datetime.date())
		manager = selected_data.user
	else:
		manager = User.objects.get(username=i['входящий номер'])
	return manager