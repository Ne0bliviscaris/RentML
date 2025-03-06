from typing import List


class Car:
    """Base class for all car types in the system."""

    name = None
    model = None
    car_type = None
    year = None
    color = None
    engine = None
    vin = None
    registration = None
    emission_standard = None
    max_load = None
    speed_limit = None
    daily_limit = 300
    seats = None

    @classmethod
    def get_all_cars(cls) -> List["Car"]:
        """Return all registered car types."""
        return [c() for c in cls.__subclasses__()]


class Scudo(Car):
    name = "Scudo"
    model = "Fiat Scudo"
    car_type = "Osobowy"
    year = 2013
    color = "Granatowy"
    engine = "2.0 Multijet 163KM"
    vin = "ZFA270000********"
    registration = "PSZ 6***0"
    emission_standard = "Euro 5"
    max_load = None
    speed_limit = 140
    seats = 9


class L3H2(Car):
    name = "L3H2"
    model = "Peugeot Boxer L3H2"
    car_type = "Dostawczy"
    year = 2011
    color = "Biały"
    engine = "2.2 HDI 120KM"
    vin = "VF3YBBMFC1********"
    registration = "PSZ 67***"
    emission_standard = "Euro 5"
    max_load = 1190
    speed_limit = 120
    seats = 3


class L4H2(Car):
    name = "L4H2"
    model = "Peugeot Boxer L4H2"
    car_type = "Dostawczy"
    year = 2010
    color = "Biały"
    engine = "3.0 HDI 160KM"
    vin = "VF3YDDMFC1********"
    registration = "PSZ 8***9"
    emission_standard = "Euro 4"
    max_load = 1439
    speed_limit = 140
    seats = 3
