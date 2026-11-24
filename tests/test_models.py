from pydantic import ValidationError
import pytest
from src.models.vehicle import Vehicle


def test_invalid_vin_length():
    with pytest.raises(ValidationError):
        Vehicle(vin="ABC123", brand="BMW", model="320i", year=2020)


def test_invalid_vin_character():
    with pytest.raises(ValidationError):
        Vehicle(vin="WVWZZZ1JZXW00000O", brand="VW", model="Golf", year=2020)


def test_invalid_vehicle_year():
    with pytest.raises(ValidationError):
        Vehicle(vin="WVWZZZ1JZXW000001", brand="VW", model="Golf", year=1800)


from src.models.part import PartRequest


def test_empty_part_name():
    with pytest.raises(ValidationError):  # Boş parça adı reddedilmeli
        PartRequest(part_name="   ")


def test_zero_quantity():
    with pytest.raises(ValidationError):  # Sıfır adet kabul edilmemeli
        PartRequest(part_name="Fren Balatası", quantity=0)


def test_negative_quantity():
    with pytest.raises(ValidationError):  # Negatif adet kabul edilmemeli
        PartRequest(part_name="Fren Balatası", quantity=-2)


from src.models.part import PartRequest


def test_empty_part_name():
    with pytest.raises(ValidationError):  # Boş parça adı reddedilmeli
        PartRequest(part_name="   ")


def test_zero_quantity():
    with pytest.raises(ValidationError):  # Sıfır adet kabul edilmemeli
        PartRequest(part_name="Fren Balatası", quantity=0)


def test_negative_quantity():
    with pytest.raises(ValidationError):  # Negatif adet kabul edilmemeli
        PartRequest(part_name="Fren Balatası", quantity=-2)


def test_valid_vehicle():
    vehicle = Vehicle(vin="WVWZZZ1JZXW000001", brand="Volkswagen", model="Golf", year=2020)
    assert vehicle.brand == "Volkswagen"  # Marka doğru kaydedilmeli
    assert vehicle.year == 2020  # Model yılı doğru olmalı


def test_valid_part_request():
    request = PartRequest(part_name="Fren Balatası", quantity=2)
    assert request.part_name == "Fren Balatası"  # Parça adı korunmalı
    assert request.quantity == 2  # Adet doğru kaydedilmeli
