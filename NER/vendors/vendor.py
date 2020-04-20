from abc import ABCMeta, abstractmethod
from enum import Enum, auto


class ChargeType(Enum):
    AIRPLANE = auto()
    GAS = auto()
    UBER = auto()
    PARKING = auto()
    HOTEL = auto()
    LODGING_TAX = auto()
    MEAL_PER_DIEM = auto()
    PHONE = auto()
    CAR_RENTAL = auto()
    CONFERENCE_FEE = auto()
    LAUNDRY = auto()

    def __str__(self):
        return {ChargeType.AIRPLANE.value: "AIRPLANE",
                ChargeType.GAS.value: "GAS",
                ChargeType.UBER.value: "UBER",
                ChargeType.PARKING.value: "PARKING",
                ChargeType.HOTEL.value: "HOTEL",
                ChargeType.LODGING_TAX.value: "LODGING_TAX",
                ChargeType.MEAL_PER_DIEM.value: "MEAL_PER_DIEM ",
                ChargeType.PHONE.value: "PHONE",
                ChargeType.CAR_RENTAL.value: "CAR_RENTAL",
                ChargeType.CONFERENCE_FEE.value: "CONFERENCE_FEE",
                ChargeType.LAUNDRY.value: "LAUNDRY"}[self.value]


class Vendor(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def matches_vendor(text):
        """@:return True if text could be parsed by this vendor"""
        return False

    @staticmethod
    @abstractmethod
    def get_vendor_name():
        """@:return string with this vendor's name"""
        return None

    @staticmethod
    @abstractmethod
    def charge_type():
        """@:return ChargeType this vendor charges"""
        raise NotImplementedError

    @abstractmethod
    def get_expense_charge(self):
        """@return float of the amount this vendor charged"""
        raise NotImplementedError

    @abstractmethod
    def get_expense_date(self):
        """@:return datetime of the date of this vendor's expense"""
        raise NotImplementedError

    @abstractmethod
    def parsed_correctly(self):
        """@return True if this object successfully parsed the the inputted text"""
        return False

    def __str__(self):
        return "Vendor named %s of type %s cost %.2f on date %s" % (self.get_vendor_name(),
                                                                    str(self.charge_type()),
                                                                    self.get_expense_charge(),
                                                                    str(self.get_expense_date()))

