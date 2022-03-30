import datetime

from flask import abort
from service.account_service import AccountService
from service.price_plan_service import PricePlanService

from .electricity_reading_controller import repository as readings_repository
account_service = AccountService()
price_plan_service = PricePlanService(readings_repository)


def compare(smart_meter_id):
    list_of_spend_against_price_plans = price_plan_service.get_list_of_spend_against_each_price_plan_for(smart_meter_id)
    if len(list_of_spend_against_price_plans) < 1:
        abort(404)
    else:
        return {
            "pricePlanId": account_service.get_price_plan(smart_meter_id),
            "pricePlanComparisons": list_of_spend_against_price_plans
        }


def recommend(smart_meter_id, limit=None):
    list_of_spend_against_price_plans = price_plan_service.get_list_of_spend_against_each_price_plan_for(smart_meter_id, limit=limit)
    return list_of_spend_against_price_plans


def last_week_costs(smart_meter_id):
    last_week = datetime.datetime.now() - datetime.timedelta(weeks=1)
    costs = price_plan_service.get_list_of_costs_in_timerange(smart_meter_id, date_from=last_week)
    total = 0
    for cost in costs:
        total += cost

    return total
