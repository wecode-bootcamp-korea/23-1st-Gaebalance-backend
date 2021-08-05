import json, re, bcrypt, jwt

from django.views        import View
from django.http         import JsonResponse, request

from users.models        import User, UserColor
from products.models     import Size, Color

from gaebalance.settings import SECRET_KEY  

email_ragular    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
password_regular = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,12}$')

class JoinView(View):
    def post(self,request):
        try:
            data =json.loads(request.body)
            bcrypt_password = bcrypt.hashpw(data["password"].encode("utf-8"),bcrypt.gensalt()). decode("utf-8")

            if (User.objects.filter(email=data["email"]).exists()) or (User.objects.filter(phone_number=data['phone_number']).exists()):
                return JsonResponse ({"MESSAGE": "EXIST_DATA"}, status = 400)

            if (not email_ragular.match(data["email"])) or (not password_regular.match(data["password"])):
                return JsonResponse ({"MESSAGE":"INVALID_FORMAT"}, status = 400)	
  
       	    user = User.objects.create(
				name         = data["name"],
				gender       = data["gender"],
				birth_date   = data["birth_date"],
				phone_number = data["phone_number"],
				email        = data["email"],
				password     = bcrypt_password,
				address      = data["address"],
				size         = Size.objects.get(id=data["size_id"])
			)  

            for color_id in data["colors_id"]:
                UserColor.objects.create(
				user  = User.objects.get(id=user.id),
				color = Color.objects.get(id=color_id)
			    )
			
            return JsonResponse ({"MESSAGE":"CREATED"}, status = 201)
				
        except KeyError:
       	    return JsonResponse ({"MESSAGE":"KEY_ERROR"}, status = 400)

class LoginView(View):
	def post(self,request):
		try:
			data = json.loads(request.body)

			if data["email"] == "" or data["password"] == "" :
				return JsonResponse ({"MESSAGE": "INVALID_REQUEST"},status = 400)	

			if not User.objects.filter(email=data['email']).exists():
				return JsonResponse ({"MESSAGE":"USER_DOES_NOT_EXIST"}, status =401)
	
			user	 = User.objects.get(email=data["email"])
			password = user.password.encode("utf-8")

			if not bcrypt.checkpw(data["password"].encode("utf-8"),password) :
				return JsonResponse ({"MESSAGE":"INVALID_PASSWORD"},status = 401)

			access_token = jwt.encode({"id": user.id}, SECRET_KEY, algorithm="HS256")
			return JsonResponse ({"access_token":"token","MESSAGE":"SUCCESS"}, status = 200)

		except KeyError:
			return JsonResponse ({"MESSAGE":"KEY_ERROR"},status = 400)	
