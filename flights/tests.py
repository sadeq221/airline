from django.test import TestCase, Client
from .models import Airport, Flight, Passenger
from django.db.models import Max

# Create your tests here.


class FlightTestCase(TestCase):

    def setUp(self):

        # Create airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create flights.
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        c = Client()
        response = c.get("/flights/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['flights'].count(), 3)
        
    def test_valid_flight_page(self):
        c = Client()
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        
    def test_invalid_flight_page(self):
        c = Client()
        max_id = Flight.objects.all().aggregate(Max('id'))['id__max']
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.templates[0].name, 'flights/404.html')
        
    def test_invalid_page(self):
        c = Client()
        response = c.get("/flights/alaki")
        self.assertEqual(response.status_code, 404)
        
    def test_flight_passengers(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        p = Passenger.objects.create(first='ali', last='rezaei')
        p.save()
        p.flights.add(f)
        self.assertEqual(f.passengers.count(), 1)