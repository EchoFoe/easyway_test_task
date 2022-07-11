from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import BusStation, Carrier, Itinerary, Voyage, Ticket
from .forms import TicketCreateForm
from .serializers import BusStationsSerializer, CarriersSerializer, ItinerariesSerializer, VoyagesSerializer, \
    TicketsSerializer


def home(request):
    return render(request, 'home/home.html')


def tickets_list(request):
    tickets = Ticket.objects.all()

    context = {
        'tickets': tickets
    }

    return render(request, 'tickets/tickets_list.html', context)


@staff_member_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.save()
            return render(request, 'tickets/ticket_created.html', {
                'ticket': ticket,
            })
    else:
        form = TicketCreateForm()

    context = {
        'form': form,
    }

    return render(request, 'tickets/ticket_create.html', context)


@staff_member_required
def ticket_admin_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    context = {
        'ticket': ticket,
    }

    return render(request, 'tickets/ticket_admin_detail.html', context)


@staff_member_required
def ticket_detail(request, ticket_number):
    ticket = get_object_or_404(Ticket, ticket_number=ticket_number)

    context = {
        'ticket': ticket,
    }

    return render(request, 'tickets/ticket_detail.html', context)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'


class BusStationList(viewsets.ModelViewSet):
    queryset = BusStation.objects.all()
    serializer_class = BusStationsSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['city', 'name']
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    search_fields = ['city', 'name']
    lookup_field = 'pk'


class CarrierList(viewsets.ModelViewSet):
    queryset = Carrier.objects.all()
    serializer_class = CarriersSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    search_fields = ['inn_number']
    lookup_field = 'pk'


class ItineraryList(viewsets.ModelViewSet):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerariesSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['departure_station', 'arrival_station']
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    search_fields = ['name', 'number']
    lookup_field = 'pk'


class VoyageList(viewsets.ModelViewSet):
    queryset = Voyage.objects.all()
    serializer_class = VoyagesSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['itinerary', 'bus_station_platform']
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    search_fields = ['itinerary__name']
    lookup_field = 'pk'


class TicketList(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketsSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['voyage', 'type_ticket']
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    search_fields = ['passengers_name', 'ticket_number']
    lookup_field = 'pk'
