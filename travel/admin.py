from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import BusStation, Carrier, Itinerary, Voyage, Ticket, PrintTemplate


def ticket_admin_detail(obj):
    return mark_safe('<a href="{}" target="_blank">Просмотр деталей</a>'.format(
        reverse('travel:ticket_admin_detail', args=[obj.id])))


ticket_admin_detail.short_description = 'Детали к билету'


@admin.register(BusStation)
class BusStationAdmin(admin.ModelAdmin):
    save_as = True
    fields = ['name', ('city', 'region')]
    list_display = ['name', 'city', 'region']
    list_display_links = ['name']
    search_fields = ['name', 'city', 'region']
    list_filter = ['city', 'region']


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    save_as = True
    fields = ['name', 'inn_number']
    list_display = ['name', 'inn_number']
    list_display_links = ['name']
    search_fields = ['name', 'inn_number']


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    save_as = True
    fields = ['name', 'number', ('departure_station', 'arrival_station')]
    list_display = ['name', 'number', 'departure_station', 'arrival_station']
    list_display_links = ['name']
    list_editable = ['departure_station', 'arrival_station']
    search_fields = ['name', 'number']


@admin.register(Voyage)
class VoyageAdmin(admin.ModelAdmin):
    save_as = True
    fields = [('departure_date', 'arrival_date'), ('itinerary', 'bus_station_platform')]
    list_display = ['departure_date', 'arrival_date', 'itinerary', 'bus_station_platform']
    list_display_links = ['departure_date']
    search_fields = ['itinerary']
    list_filter = ['itinerary']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    save_as = True
    fields = [('passengers_name', 'voyage'), ('ticket_number', 'place_number', 'type_ticket')]
    list_display = ['passengers_name', 'voyage', 'ticket_number', 'place_number', 'type_ticket', ticket_admin_detail]
    list_display_links = ['passengers_name']
    list_editable = ['ticket_number', 'place_number', 'type_ticket']
    search_fields = ['passengers_name']
    list_filter = ['voyage', 'type_ticket']


@admin.register(PrintTemplate)
class PrintTemplateAdmin(admin.ModelAdmin):
    save_as = True
    fieldsets = (
        ('Название для шаблона печати', {
            'fields': ('name',),
        }),
        ('Билет', {
            # "classes": ("collapse",),
            'fields': [('passengers_name', 'ticket_number', 'place_number', 'type_ticket')],
        }),
        ('Рейс', {
            # "classes": ("collapse",),
            'fields': [('voyage->departure_date', 'voyage->arrival_date', 'voyage->bus_station_platform')],
        }),
        ('Маршрут', {
            # "classes": ("collapse",),
            'fields': [('voyage->itinerary->name', 'voyage->itinerary->number')],
        }),
        ('Станция отправления', {
            # "classes": ("collapse",),
            'fields': [('voyage->itinerary->departure_station->name',
                        'voyage->itinerary->departure_station->city', 'voyage->itinerary->departure_station->region')],
        }),
        ('Станция прибытия', {
            # "classes": ("collapse",),
            'fields': [('voyage->itinerary->arrival_station->name',
                        'voyage->itinerary->arrival_station->city', 'voyage->itinerary->arrival_station->region')],
        }),
    )
