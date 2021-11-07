from jinja2 import Environment, filters
from flask import request

def datetimeformat(value, format='%H:%M %d/%m/%Y'):
    return value.strftime(format)

def combine_shorten_url(shorten_url):
    return request.host_url + shorten_url

# env = Environment()
filters.FILTERS['datetimeformat'] = datetimeformat
filters.FILTERS['combine_shorten_url'] = combine_shorten_url
# env.filters['datetimeformat'] = datetimeformat