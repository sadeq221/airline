from django.shortcuts import render
from .models import Flight, Passenger
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request, 'flights/index.html', {
        'flights': Flight.objects.all()
    })


def flight(request, flight_id):
    if flight := Flight.objects.filter(pk=flight_id).first():
        return render(request, 'flights/flight.html', {
            'flight': flight,
            'passengers': flight.passengers.all(),
            'non_passengers': Passenger.objects.exclude(flights=flight).all()
            })
    else:
        return render(request, 'flights/404.html')


def book(request, flight_id):
    if request.method == 'POST':
        flight = Flight.objects.filter(pk=flight_id).first()
        passenger = Passenger.objects.filter(pk=int(request.POST['passenger'])).first()

        passenger.flights.add(flight)
        
        return HttpResponseRedirect(reverse("flight", args=[flight.id]))
