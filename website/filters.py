from jinja2 import Environment, filters

def datetimeformat(value, format='%H:%M %d/%m/%Y'):
    return value.strftime(format)

# env = Environment()
filters.FILTERS['datetimeformat'] = datetimeformat
# env.filters['datetimeformat'] = datetimeformat