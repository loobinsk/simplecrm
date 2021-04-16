from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify


CALL_STATUS = (
	(0, 'отвеченно'),
	(1, 'Не дозвонился'),
	(2, 'Занято'),
)

class Client(models.Model):
	''' Карточка клиента '''
	curator = models.ForeignKey(User, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=255, blank=True)
	phone = models.CharField(max_length=255)
	email = models.EmailField(blank=True)
	call_source = models.CharField(max_length=255, default='не определен')
	current_situation = models.TextField(blank=True)
	desired_situation = models.TextField(blank=True)
	other_options = models.TextField(blank=True)
	main_motive = models.TextField(blank=True)
	proposed = models.TextField(blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(max_length=255, default=f'slug', blank=True)

	class Meta:
		ordering = ('-create_date',)
		verbose_name = 'клиент'
		verbose_name_plural = 'Клиенты'

	def get_source_name(self):
		return CALL_SOURCE[self.call_source][1]

	def get_name(self):
		return f'клиент номер {self.id}'

	def __str__(self):
		if self.full_name:
			return self.full_name
		else:
			return self.get_name()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.phone)
		super(Client, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('client_detail', args=[self.slug])

class Call(models.Model):
	''' Звонок клиента '''
	client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='calls')
	url = models.FileField(upload_to='records/%m/')
	call_date = models.DateTimeField()
	manager = models.ForeignKey(User, on_delete=models.CASCADE)
	call_status = models.SmallIntegerField(choices=CALL_STATUS, blank=True, default=0)

	def get_data(self):
		data = self.call_date.strftime("%Y-%m-%dT%H:%M:%S+0000")
		return data

	class Meta:
		ordering = ('-call_date',)
		verbose_name = 'Звонок'
		verbose_name_plural = 'Звонки'

	def get_name(self):
		return f'Звонок с номера +7{self.client.phone}'

	def __str__(self):
		return f'Звонок с номера +7{self.client.phone}'

class CallComment(models.Model):
	'''Комментарий к звонку'''
	call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField(max_length=500)
	create_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('call',)
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'

	def __str__(self):
		return f'{self.author.username}, {self.call.client.get_name()}, {self.text}'

class SelectedData(models.Model):
	user = models.CharField(max_length=255)
	data1 = models.DateField()

	def user_name(self):
		return self.user.first_name

	def data(self):
		data = self.data1.strftime("%Y-%m-%d")
		return data

class Ddd(models.Model):
	name = models.TextField()
	name2 = models.CharField(max_length=234)