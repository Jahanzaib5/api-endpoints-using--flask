"""API endpoints for countries and stats"""
from collections import defaultdict
from typing import Dict, List, Any, DefaultDict

from flask import Blueprint, request
from sqlalchemy import or_, func, tuple_, select, text, create_engine
from sqlalchemy.orm import sessionmaker
from models import Country, Indicator, Aggregate

stats_api_bp = Blueprint("country_stats", __name__, url_prefix="/api")

@stats_api_bp.route("/indicators")
def indicators_list():
    """All indicators list"""
    indicators = Indicator.query.distinct(Indicator.indicator_id).all()
    indicators_details = {}
    for ind in indicators:
        indicators_details[ind.indicator_id] = {
            "api_code": ind.indicator_api_code,
            "name": ind.indicator_name,
            "description": ind.indicator_description,
            "source": ind.indicator_source,
            "topics": ind.indicator_topic,
        }
    return indicators_details

@stats_api_bp.route("/regions/")
def regions_list():
    """All regions list"""
#    aggregates = Aggregate.query.distinct(Aggregate.aggregate_id).all()
    aggregates = Aggregate.query.all()
    aggregates_details = {}
    for agg in aggregates:
        print(' voilaaao')
        print(agg)
        aggregates_details[agg.aggregate_name] = {
            "aggregate_id" : agg.aggregate_id,
            "aggregate_isoid" : agg.aggregate_isoid,
            "description": agg.aggregate_description,
        }
    return aggregates_details

#---------------------------------------- HERE FOR MODIFICATION IN FIVER!! ----------------------------------------#
@stats_api_bp.route("/regions/<region_id>")
def regions_stats(region_id):
    """All regions list"""

    # aggregates = Aggregate.query.filter(Aggregate.aggregate_isoid == region_id)
    # indicators = Indicator.query.filter(Indicator.country_id.in_(aggregates))

    statement = text("""SELECT SUM(indicator_value),year, indicator_id FROM indicatordb WHERE country_id IN (SELECT country_id FROM aggregatedb WHERE aggregate_isoid = region_isoid) GROUP BY year,indicator_id ORDER BY indicator_id, year""")
    
    

    result = {}

    # for indic in indicators:
    #     result[indic.indicator_name]={
    #         "indicator_value":func.sum(indic.indicator_value),
    #         "year":indic.year,
    #         "indicator_id":indic.indicator_id,
    #     }

    return result

@stats_api_bp.route("/countries/")
def countries():
    """All countries list"""
    res_countries = Country.query.all()
    print(res_countries)
    return {"countries": [c.res_dict() for c in res_countries]}

@stats_api_bp.route("/countries/<country_id_or_name>")
def country(country_id_or_name):
    """Country by ID or Name or ISOCode"""
    country_res = get_country_by_id_or_name(country_id_or_name)
    return country_res.res_dict()

@stats_api_bp.route("/countries/<country_id_or_name>/stats")
def country_stats(country_id_or_name):
    """stats for a country

    indicator_ids - get parameter to specify list of indicators
    (if not specified - all indicators)"""
    country_res = get_country_by_id_or_name(country_id_or_name)
    res_dict = {"country_id": country_res.country_id}

    indicators_query = Indicator.query.filter(
        Indicator.country_id == country_res.country_id
    ).order_by(Indicator.year)

    years = [int(i.year) for i in indicators_query.distinct(Indicator.year).all()]
    res_dict["years"] = years
    years_num_dict: Dict[int, int] = {v: k for k, v in enumerate(years)}

    indicators = indicators_query.all()
    indicators_dict: DefaultDict[str, List[Any]] = defaultdict(
        lambda: [None] * len(years)
    )

    for ind in indicators:
        year_index: int = years_num_dict[ind.year]
        indicators_dict[ind.indicator_id][year_index] = float(ind.indicator_value)
    res_dict["indicator_values"] = indicators_dict

    return res_dict


def get_country_by_id_or_name(country_id_or_name):
    """helper function to get country by id or name or iso code"""
    try:
        country_id = int(country_id_or_name)
        country_query = Country.query.filter(Country.country_id == country_id)
    except ValueError:
        country_query = Country.query.filter(
            or_(
                Country.country_name == country_id_or_name,
                Country.country_isoid == country_id_or_name,
            )
        )
    return country_query.first_or_404(
        description='Country "{}" not found'.format(country_id_or_name)
    )




sql = text('SELECT SUM(indicator_value),year, indicator_id FROM indicatordb WHERE country_id IN (SELECT country_id FROM aggregatedb WHERE aggregate_isoid = region_isoid) GROUP BY year,indicator_id ORDER BY indicator_id, year')
#result = session.execute(sql)

