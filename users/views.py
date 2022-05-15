import json
from django.http import JsonResponse
from django.shortcuts import render
from passlib.hash import pbkdf2_sha256
from healthfit.settings import usersDb
import uuid
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        full_name = data.get("full_name")
        email = data.get("email")
        mobile = data.get("mobile")
        password = data.get("password")
        hash = pbkdf2_sha256.hash(password)
        auth_token = str(uuid.uuid4())
        res = usersDb.find({"email": email})
        if not(list(res)):
            resp = usersDb.insert_one({
                "_id": str(uuid.uuid4())[-12:],
                "full_name": full_name,
                "email": email,
                "mobile": mobile,
                "hash_password" : hash,
                "auth_token" : auth_token
            })
            return JsonResponse({"status": 1}, safe=False)
        else:
            return JsonResponse({"status": -1, "msg":"User already present"}, safe=False)

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        email = data.get("email")
        password = data.get("password")
        res = list(usersDb.find({"email": email}))
        if res:
            res = res[0]
            auth = pbkdf2_sha256.verify(password, res.pop('hash_password'))
            if auth:

                return JsonResponse({"status":1, "user":res}, safe=False)
            else:
                return JsonResponse({"status": -1, "msg": "Wrong email or password"}, safe=False)
        else:
            return JsonResponse({"status": -1, "msg":"User not found"}, safe=False)