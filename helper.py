import traceback
import datetime
from zoneinfo import ZoneInfo
# def handle_errors(cls):
#     """
#     Class decorator to handle all errors in a class.
#     """
#     def wrap_methods(method):
#         """
#         Decorator function to wrap each method in the class with error handling.
#         """
#         def wrapped(*args, **kwargs):
#             try:
#                 return {
#                     'status' : True,
#                     'message': "Success",
#                     'data'   : method(*args, **kwargs)
#                 }
#             except Exception as e:
#                 return {
#                     'status' : False,
#                     'message': f"Error in {cls.__name__}.{method.__name__}: {e}",
#                     'data'   : traceback.format_exc()
#                 }
#         return wrapped

#     for name, method in vars(cls).items():
#         if callable(method):
#             setattr(cls, name, wrap_methods(method))

#     return cls


import traceback

def handle_errors(obj):
    """
    Decorator to handle all errors in a function or class.
    """
    if isinstance(obj, type):
        # Handle class
        def wrap_methods(method):
            """
            Decorator function to wrap each method in the class with error handling.
            """
            def wrapped(*args, **kwargs):
                try:
                    return {
                        'status' : True,
                        'message': "Success",
                        'data'   : method(*args, **kwargs)
                    }
                except Exception as e:
                    return {
                        'status' : False,
                        'message': f"Error in {obj.__name__}.{method.__name__}: {e}",
                        'data'   : traceback.format_exc()
                    }
            return wrapped

        for name, method in vars(obj).items():
            if callable(method):
                setattr(obj, name, wrap_methods(method))

        return obj

    else:
        print("HERE")
        # Handle function
        def wrapped(*args, **kwargs):
            try:
                return {
                    'status' : True,
                    'message': "Success",
                    'data'   : obj(*args, **kwargs)
                }
            except Exception as e:
                return {
                    'status' : False,
                    'message': f"Error in {obj.__name__}: {e}",
                    'data'   : traceback.format_exc()
                }
        return wrapped

# This code defines a function called getFreshTimeStamp that returns
# the current time in a specified timezone and format.
# ---------------------------------------
def getFreshTimeStamp(dateFormat: str = "%Y-%m-%d %H:%M:%S", timezone: str ="UTC") -> str:
    """
    Get the current time in the specified timezone and format.

    Args:
        format (str, optional): The format of the timestamp. Defaults to "%Y-%m-%d %H:%M:%S".
        timezone (str, optional): The timezone of the timestamp. Defaults to "UTC".

    Returns:
        str: The current time in the specified format.

    Usage:
        ```
        getFreshTimeStamp()
        getFreshTimeStamp(dateFormat="%d/%m/%Y %H:%M:%S")
        getFreshTimeStamp(dateFormat="iso8601")
        getFreshTimeStamp(dateFormat="iso8601", timezone="America/New_York")
        ```
    """

    # Get the current time in the specified timezone
    # now = datetime.datetime.now(pytz.timezone(timezone))
    now = datetime.datetime.now(ZoneInfo(timezone))

    # If the format is set to 'iso8601', change it to the appropriate format for ISO 8601
    if dateFormat == "iso8601":
        dateFormat = "%Y-%m-%dT%H:%M:%SZ"

    # Return the current time in the specified format
    return now.strftime(dateFormat)

# Convert a given date from one timezone to another timezone and format it.
# The function returns the converted date in the specified format.
# ---------------------------------------------
def convertTimezone(date: str, FromTimeZone: str, ToTimeZone: str, dateFormat="%Y-%m-%d %H:%M:%S") -> str:
    """
    Convert a given date from one timezone to another timezone and format it.

    Args:
        date (str): The date to be converted.
        FromTimeZone (str): The timezone of the given date.
        ToTimeZone (str): The timezone to which the date should be converted.
        dateFormat (str, optional): The format of the date. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The converted date in the specified format.

    Usage:
        ```
        convertTimezone("2024-06-06 09:11:50", "UTC", "America/New_York")
        convertTimezone("2024-06-06 09:11:50", "UTC", "America/New_York", dateFormat="iso8601")
        convertTimezone(date="2024-06-06 09:11:50", FromTimeZone="UTC", ToTimeZone="America/New_York", dateFormat="%d/%m/%Y %H:%M:%S")
        ```
    """

    # If the format is set to 'iso8601', change it to the appropriate format for ISO 8601
    if dateFormat == "iso8601":
        dateFormat = "%Y-%m-%dT%H:%M:%SZ"

    #  create a datetime object using the given date string and date format
    datetime_obj       = datetime.datetime.strptime(date, dateFormat)

    # replace the timezone information with the specified FromTimeZone.
    datetime_obj       = datetime_obj.replace(tzinfo=ZoneInfo(FromTimeZone))

    # convert the date to the specified time zone.
    converted_datetime = datetime_obj.astimezone(ZoneInfo(ToTimeZone))

    # format the result uing specified format
    formatted_datetime = converted_datetime.strftime(dateFormat)

    return formatted_datetime