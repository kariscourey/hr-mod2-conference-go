from datetime import datetime
from json import JSONEncoder

from django.db.models import QuerySet


class DateEncoder(JSONEncoder):
    def default(self, o):
        # if o is an instance of datetime
        if isinstance(o, datetime):
            # return o.isoformat()
            return o.isoformat()
        # otherwise
        else:
            # return super().default(o)
            return super().default(o)


class QuerySetEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return list(o)
        else:
            return super().default(o)


class ModelEncoder(DateEncoder, QuerySetEncoder, JSONEncoder):

    # create empty encoders dictionary that will hold property-encodername k-vs
    encoders = {}

    def default(self, o):
        # if the object to decode is the same class as what's in the
        # model property, then
        if isinstance(o, self.model):
            # create an empty dictionary that will hold the property names
            # as keys and the property values as values
            d = {}

            # if o has the attribute get_api_url
            if hasattr(o, "get_api_url"):
                # then add its return value to the dictionary
                # with the key "href"
                d["href"] = o.get_api_url()

            # for each name in the properties list
            for property in self.properties:
                # get the value of that property from the model instance
                # given just the property name
                value = getattr(o, property)

                # check if property is in self.encoders attribute
                if property in self.encoders:
                    # store value of property (encoder name)
                    encoder = self.encoders[property]
                    # set value (to add to d) to #TODO - understand
                    value = encoder.default(value)

                # put it into the dictionary with that property name as
                # the key
                d[property] = value

            # update dictionary per get_extra_data (where o is the key)
            d.update(self.get_extra_data(o))

            # return the dictionary
            return d
        # otherwise
        else:
            # return super().default(o)  # From the documentation
            return super().default(o)

    # wherever you want to add extra data, you only need to add that
    # method to the specific model encoder that you're building
    def get_extra_data(self, o):
        # return empty dict (if not overridden within encoder)
        return {}
