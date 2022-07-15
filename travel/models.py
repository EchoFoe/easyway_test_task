from django.db import models
from django.urls import reverse
from django.utils import timezone


class BaseContent(models.Model):
    created = models.DateField(blank=True, null=True, default=timezone.now, verbose_name='Дата создания записи')
    updated = models.DateField(blank=True, null=True, auto_now=True, verbose_name='Дата ред-ия записи')

    class Meta:
        abstract = True


class BusStation(models.Model):
    name = models.CharField(max_length=64, verbose_name='Наименование автостанции')
    city = models.CharField(max_length=32, verbose_name='Город')
    region = models.CharField(max_length=32, verbose_name='Регион')

    class Meta:
        ordering = ['name']
        verbose_name = 'Автостанция'
        verbose_name_plural = 'Автостанции'

    def __str__(self):
        return '%s (%s/%s)' % (self.name, self.city, self.region)


class Carrier(models.Model):
    name = models.CharField(max_length=64, verbose_name='Наименование перевозчика')
    inn_number = models.PositiveBigIntegerField(verbose_name='ИНН', unique=True,
                                                help_text='Идентификационный номер налогоплательщика')

    class Meta:
        ordering = ['name']
        verbose_name = 'Перевозчик'
        verbose_name_plural = 'Перевозчики'

    def __str__(self):
        return '%s, ИНН: %s' % (self.name, self.inn_number)


class Itinerary(models.Model):
    name = models.CharField(max_length=64, verbose_name='Наименование маршрута')
    number = models.CharField(max_length=64, verbose_name='Номер маршрута')
    departure_station = models.ForeignKey(BusStation, related_name='departure_busstations', on_delete=models.CASCADE,
                                          verbose_name='Станция отправления')
    arrival_station = models.ForeignKey(BusStation, related_name='arrival_bus_stations', on_delete=models.CASCADE,
                                        verbose_name='Станция прибытия')

    class Meta:
        ordering = ['name']
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return '%s (%s -> %s)' % (self.name, self.departure_station, self.arrival_station)


class Voyage(models.Model):
    departure_date = models.DateTimeField(verbose_name='Дата отправления')
    arrival_date = models.DateTimeField(verbose_name='Дата прибытия')
    itinerary = models.ForeignKey(Itinerary, related_name='itineraries', on_delete=models.CASCADE,
                                  verbose_name='Маршрут')
    bus_station_platform = models.PositiveIntegerField(verbose_name='Платформа автостанции')

    class Meta:
        ordering = ['departure_date']
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'

    def __str__(self):
        return '%s' % self.itinerary


class Ticket(models.Model):
    TYPE_TICKET = [
        ('Взрослый билет', 'Взрослый билет'),
        ('Детский билет', 'Детский билет'),
    ]

    passengers_name = models.CharField(max_length=128, verbose_name='ФИО пассажира')
    voyage = models.ForeignKey(Voyage, related_name='voyages', on_delete=models.CASCADE, verbose_name='Рейс')
    ticket_number = models.CharField(max_length=32, unique=True, verbose_name='Номер билета')
    place_number = models.PositiveSmallIntegerField(verbose_name='Номер места')
    type_ticket = models.CharField(max_length=256, choices=TYPE_TICKET, verbose_name='Тип билета')

    class Meta:
        ordering = ['passengers_name']
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'

    def get_absolute_url(self):
        return reverse('travel:ticket_detail', args=[self.ticket_number])

    def get_fields_from_model(self):
        return [f.name for f in Ticket._meta.local_fields]

    def __str__(self):
        return '№ билета: %s, ФИО пассажира: %s' % (self.ticket_number, self.passengers_name)


ticket_meta_fields = Ticket._meta.fields


def get_all_fields_of_ticket(prefix='', fields=ticket_meta_fields):

    def create_prefix(prefix):
        if prefix == '':
            return ''
        return prefix + '->'

    ticket_fields_list = []
    for f in fields:
        if f.name == "id":
            pass
        elif type(f) == models.fields.related.ForeignKey:
            ticket_fields_list.extend(get_all_fields_of_ticket(create_prefix(prefix) + f.name,
                                                               f.remote_field.model._meta.fields))
        else:
            ticket_fields_list.append(create_prefix(prefix) + f.name)
    return ticket_fields_list


get_count_of_the_ticket_fields = len(get_all_fields_of_ticket())


class PrintTemplate(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название шаблона для печати', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Шаблон для печати'
        verbose_name_plural = 'Шаблоны для печати'

    def __str__(self):
        return 'Шаблон для печати: %s' % self.name

    def get_absolute_url(self):
        return reverse('travel:template_detail', args=[self.id])


for label in list(get_all_fields_of_ticket()):
    PrintTemplate.add_to_class(label, models.BooleanField(blank=True, default=False))
