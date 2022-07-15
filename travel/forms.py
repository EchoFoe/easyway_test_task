from django import forms
from .models import Ticket, PrintTemplate


class TicketCreateForm(forms.ModelForm):
    # passengers_name = forms.CharField(required=True, label='ФИО пассажира')
    # voyage = forms.ModelChoiceField(queryset=Voyage.objects.all(), required=True, label='Рейс')
    # ticket_number = forms.EmailField(required=True, label='Номер билета')
    # place_number = forms.CharField(required=True)
    # type_ticket = forms.ModelChoiceField(required=True)

    class Meta:
        model = Ticket
        fields = ['passengers_name', 'voyage', 'ticket_number', 'place_number', 'type_ticket']


class PrintTemplateForm(forms.ModelForm):

    class Meta:
        model = PrintTemplate
        fields = '__all__'
