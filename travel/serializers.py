from rest_framework import serializers
from .models import BusStation, Carrier, Itinerary, Voyage, Ticket, PrintTemplate


class BusStationsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='travel:busstation-detail')

    class Meta:
        model = BusStation
        fields = ('url', 'pk', 'name', 'city', 'region')


class CarriersSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='travel:carrier-detail')

    class Meta:
        model = Carrier
        fields = ('url', 'pk', 'name', 'inn_number')


class ItinerariesSerializer(serializers.ModelSerializer):
    # departure_station_name = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='travel:itinerary-detail')

    class Meta:
        model = Itinerary
        fields = ('url', 'pk', 'name', 'number', 'departure_station', 'arrival_station')

    def get_departure_station_name(self, obj):
        return '%s (id=%s)' % (obj.departure_station.name, obj.departure_station.pk)


class VoyagesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='travel:voyage-detail')

    class Meta:
        model = Voyage
        fields = ('url', 'pk', 'departure_date', 'arrival_date', 'itinerary', 'bus_station_platform')


class TicketsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='travel:ticket-detail')

    class Meta:
        model = Ticket
        fields = ('url', 'pk', 'passengers_name', 'voyage', 'ticket_number', 'place_number', 'type_ticket')


class PrintTemplateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='travel:print_template-detail')

    class Meta:
        model = PrintTemplate
        fields = ('url', 'pk', 'passengers_name', 'ticket_number', 'place_number', 'type_ticket',
                  'voyage->departure_date', 'voyage->arrival_date', 'voyage->bus_station_platform',
                  'voyage->itinerary->name', 'voyage->itinerary->number', 'voyage->itinerary->departure_station->name',
                  'voyage->itinerary->departure_station->city', 'voyage->itinerary->departure_station->region',
                  'voyage->itinerary->arrival_station->name', 'voyage->itinerary->arrival_station->city',
                  'voyage->itinerary->arrival_station->region')
