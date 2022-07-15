from django.shortcuts import render, get_object_or_404
from django.db import models
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import BusStation, Carrier, Itinerary, Voyage, Ticket, PrintTemplate
from .forms import TicketCreateForm, PrintTemplateForm
from .serializers import BusStationsSerializer, CarriersSerializer, ItinerariesSerializer, VoyagesSerializer, \
    TicketsSerializer, PrintTemplateSerializer


def home(request):
    return render(request, 'home/home.html')


def template_list(request):
    all_fields_of_tickets = [f.name for f in Ticket._meta.fields]
    ticket_str = Ticket._meta.__str__()
    templates = PrintTemplate.objects.all()
    ticket_meta_fields = Ticket._meta.fields

    def get_all_fields_of_ticket(prefix='', fields=ticket_meta_fields):

        def create_prefix(prefix):
            if prefix == '':
                return ''
            return prefix + '->'

        ticket_fields_list = []
        for f in fields:
            if f.verbose_name == "ID":
                pass
            elif type(f) == models.fields.related.ForeignKey:
                ticket_fields_list.extend(get_all_fields_of_ticket(f.verbose_name[-1],
                                                                   f.remote_field.model._meta.fields))
            else:
                ticket_fields_list.append(f.verbose_name)
        return ticket_fields_list
    get_all_fields_of_ticket = get_all_fields_of_ticket()
    get_count_of_the_ticket_fields = len(get_all_fields_of_ticket)

    def get_all_fields_of_ticket_name(prefix='', fields=ticket_meta_fields):

        def create_prefix(prefix):
            if prefix == '':
                return ''
            return prefix + '_'

        ticket_fields_list = []
        for f in fields:
            if f.name == "id":
                pass
            elif type(f) == models.fields.related.ForeignKey:
                ticket_fields_list.extend(get_all_fields_of_ticket_name(create_prefix(prefix) + f.name,
                                                                        f.remote_field.model._meta.fields))
            else:
                ticket_fields_list.append(create_prefix(prefix) + f.name)
        return ticket_fields_list
    get_all_fields_of_ticket_name = get_all_fields_of_ticket_name()

    json = {
        ticket_str: all_fields_of_tickets,
    }
    form = PrintTemplateForm(request.POST or None, initial={'data': json})
    if form.is_valid():
        pass

    context = {
        'form': form,
        'templates': templates,
        'get_all_fields_of_ticket': get_all_fields_of_ticket,
        'get_count_of_the_ticket_fields': get_count_of_the_ticket_fields,
        'get_all_fields_of_ticket_name': get_all_fields_of_ticket_name,
    }

    return render(request, 'print_templates/template_list.html', context)


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
def template_create(request):
    if request.method == 'POST':
        form = PrintTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.save()
            return render(request, 'print_templates/template_created.html', {
                'template': template,
            })
    else:
        form = PrintTemplateForm()

    context = {
        'form': form,
    }

    return render(request, 'print_templates/template_create.html', context)


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


class PrintTemplateList(viewsets.ModelViewSet):
    queryset = PrintTemplate.objects.all()
    serializer_class = PrintTemplateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    lookup_field = 'pk'
