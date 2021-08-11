import jwt

from django.http.response   import JsonResponse
from users.models           import User
from gaebalance.settings    import SECRET_KEY
from django.core.exceptions import ObjectDoesNotExist


def login_decorator(func): 
    def wrapper(self, request, *args, **kwargs) :
        try:
            token         = request.headers.get("Authorization", None)
            payload       = jwt.decode(token,SECRET_KEY, algorithms='HS256')
            request.user  = User.objects.get(id = payload["id"]) 
            return func(self, request, *args, **kwargs)   

        except jwt.exceptions.DecodeError:
            return JsonResponse({"MESSAGE" :"INVALID_TOKEN"}, status = 401)

        except User.DoesNotExist: 
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status = 401) 

    return wrapper