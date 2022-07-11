from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'api/busstations', views.BusStationList, basename='busstation')
router.register(r'api/carriers', views.CarrierList, basename='carrier')
router.register(r'api/itineraries', views.ItineraryList, basename='itinerary')
router.register(r'api/voyages', views.VoyageList, basename='voyage')
router.register(r'api/tickets', views.TicketList, basename='ticket')

app_name = 'travel'

urlpatterns = [
    path('', views.home, name='home'),
    path('tickets/', views.tickets_list, name='tickets'),
    path('tickets/ticket_detail/<int:ticket_number>/', views.ticket_detail,
         name='ticket_detail'),
    path('tickets/ticket_detail_admin/<int:ticket_id>/', views.ticket_admin_detail,
         name='ticket_admin_detail'),
    path('ticket_create/', views.ticket_create, name='ticket_create'),
    path('', include(router.urls,)),
    path('api/busstations/', views.BusStationList.as_view({'get': 'list'}), name='api_busstations'),
    path('api/carriers/', views.CarrierList.as_view({'get': 'list'}), name='api_carriers'),
    path('api/itineraries/', views.ItineraryList.as_view({'get': 'list'}), name='api_itineraries'),
    path('api/voyages/', views.VoyageList.as_view({'get': 'list'}), name='api_voyages'),
    path('api/tickets/', views.TicketList.as_view({'get': 'list'}), name='api_tickets'),
]
urlpatterns += router.urls
