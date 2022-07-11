from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import BusStation, Carrier, Itinerary, Voyage, Ticket


def ticket_admin_detail(obj):
    return mark_safe('<a href="{}" target="_blank">Просмотр деталей</a>'.format(
        reverse('travel:ticket_admin_detail', args=[obj.id])))


ticket_admin_detail.short_description = 'Детали к билету'


@admin.register(BusStation)
class BusStationAdmin(admin.ModelAdmin):
    save_as = True
    fields = ['name', ('city', 'region'), ('created', 'updated')]
    list_display = ['name', 'city', 'region', 'created']
    list_display_links = ['name']
    search_fields = ['name', 'city', 'region']
    list_filter = ['city', 'region']
    date_hierarchy = 'created'
    readonly_fields = ['created', 'updated']


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    save_as = True
    fields = ['name', 'inn_number', ('created', 'updated')]
    list_display = ['name', 'inn_number', 'created']
    list_display_links = ['name']
    search_fields = ['name', 'inn_number']
    date_hierarchy = 'created'
    readonly_fields = ['created', 'updated']


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    save_as = True
    fields = ['name', 'number', ('departure_station', 'arrival_station'), ('created', 'updated')]
    list_display = ['name', 'number', 'departure_station', 'arrival_station']
    list_display_links = ['name']
    list_editable = ['departure_station', 'arrival_station']
    search_fields = ['name', 'number']
    date_hierarchy = 'created'
    readonly_fields = ['created', 'updated']


@admin.register(Voyage)
class VoyageAdmin(admin.ModelAdmin):
    save_as = True
    fields = [('departure_date', 'arrival_date'), ('itinerary', 'bus_station_platform'), ('created', 'updated')]
    list_display = ['departure_date', 'arrival_date', 'itinerary', 'bus_station_platform']
    list_display_links = ['departure_date']
    search_fields = ['itinerary']
    list_filter = ['itinerary']
    date_hierarchy = 'created'
    readonly_fields = ['created', 'updated']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    save_as = True
    fields = [('passengers_name', 'voyage'), ('ticket_number', 'place_number', 'type_ticket'), ('created', 'updated')]
    list_display = ['passengers_name', 'voyage', 'ticket_number', 'place_number', 'type_ticket', ticket_admin_detail]
    list_display_links = ['passengers_name']
    list_editable = ['ticket_number', 'place_number', 'type_ticket']
    search_fields = ['passengers_name']
    list_filter = ['voyage', 'type_ticket']
    date_hierarchy = 'created'
    readonly_fields = ['created', 'updated']
