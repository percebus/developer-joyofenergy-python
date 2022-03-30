
# Story #2345
Feature: Display Cost of Last Week's Usage

  Background:
    Given Usage data stored

  Scenario Outline: a smart_meter_id with price plan
    Given I have a <smart_meter_id>
      And a <price_plan> attached to it
     When I request the usage cost
     Then I am shown the correct <total_cost> of <last_week>'s usage
  Examples:
  | week | last_week | smart_meter_id | price_plan   | price | total_cost |
  |    2 |         1 | smart-meter-0  | price-plan-0 |    10 |         10 |
  |    2 |         1 | smart-meter-1  | price-plan-1 |     2 |         20 |
  |    2 |         1 | smart-meter-2  | price-plan-0 |    10 |         30 |


#  Scenario: smart meter ID without a price plan
#    Given I have a smart meter <ID>
#    And a <price_plan> attached to it
#    And <usage> data stored
#    When I request the usage_cost
#    Then I am shown the <correct_cost> of last week's usage
