import datetime
from pprint import pprint

from aloe import before, step, world


from src.service.time_converter import iso_format_to_unix_time
from src.domain.price_plan import PricePlan
from src.repository.price_plan_repository import PricePlanRepository
from src.repository.electricity_reading_repository import ElectricityReadingRepository
from src.service.electricity_reading_service import ElectricityReadingService
from src.service.price_plan_service import PricePlanService
from src.controller.price_plan_comparator_controller import last_week_costs


DEBUG = True
last_week = datetime.datetime.now() - datetime.timedelta(weeks=1)


oElectricityReadingRepository = ElectricityReadingRepository()
oElectricityReadingService = ElectricityReadingService(oElectricityReadingRepository)
oPricePlanRepository = PricePlanRepository()
oPricePlanService = PricePlanService(oElectricityReadingRepository)
oPricePlanRepository.store([
    PricePlan('price-plan-0', "Dr Evil's Dark Energy", 10),
    PricePlan('price-plan-1', "The Green Eco"        ,  2),
    PricePlan('price-plan-2', "Power for Everyone"   ,  1)
])


@before.each_feature
def before_feature(self):
    print('price-plan-*')
    pprint(oPricePlanRepository)


def generate_timestamp(seconds=0):
    _datetime = last_week + datetime.timedelta(seconds=seconds)
    return iso_format_to_unix_time(_datetime.isoformat())


@step("Usage data stored")
def step_impl(self):
    oElectricityReadingRepository.store('smart-meter-0', [
        {'time':generate_timestamp(1), 'reading':1},
        {'time':generate_timestamp(2), 'reading':2},
        {'time':generate_timestamp(3), 'reading':3},
    ])

    oElectricityReadingRepository.store('smart-meter-1', [
        {'time':generate_timestamp(1), 'reading':4},
        {'time':generate_timestamp(2), 'reading':5},
        {'time':generate_timestamp(3), 'reading':6},
    ])

    oElectricityReadingRepository.store('smart-meter-2', [
        {'time':generate_timestamp(1), 'reading':7},
        {'time':generate_timestamp(2), 'reading':8},
        {'time':generate_timestamp(3), 'reading':9},
    ])


@step("I have a (?P<smart_meter_id>.+)")
def step_impl(self, smart_meter_id):
    world.smart_meter_id = smart_meter_id
    readings = oElectricityReadingRepository.find(smart_meter_id)
    if DEBUG is True:
        print(smart_meter_id)
        pprint(readings)


@step("a (?P<price_plan>.+) attached to it")
def step_impl(self, price_plan):
    world.price_plan = price_plan


@step("I request the usage cost")
def step_impl(self):
    world.result = last_week_costs(world.smart_meter_id)


@step("I am shown the correct (?P<total_cost>.+) of (?P<last_week>.+)'s usage")
def step_impl(self, total_cost, last_week):
    world.expected = float(total_cost)
    assert world.expected == world.result, f'expected:{world.expected}, got:{world.result}'
