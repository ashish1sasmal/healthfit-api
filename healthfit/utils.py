from functools import wraps

from django.http import JsonResponse
from healthfit.settings import usersDb


def login_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        user = list(usersDb.find({"auth_token": request.headers.get("Auth-token")}))
        if user:
            request.user = user[0]
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({"status": 403, "msg": "User not authorized"})

    return wrap


def shield(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as err:
            print(str(err))
            return JsonResponse({"status": -1, "msg": "Something went wrong"})

    return wrap
