import dataclasses
from django.http import JsonResponse
from django.shortcuts import render
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from healthfit.settings import *
import uuid
from datetime import datetime
import os
import requests

from healthfit.utils import login_required

# Create your views here.


@csrf_exempt
@login_required
def payments(request):
    data = json.loads(request.body)
    print(data)
    amount = 50000
    name = data.get("name")
    spec = data.get("spec")
    mobile = data.get("mobile")
    symptoms = data.get("symptoms")
    doc_id = data.get("doc_id")
    currency = "INR"
    try:
        razorpay_client = razorpay.Client(
            auth=(os.environ.get("RAZORPAY_KEY_ID"), os.environ.get("RAZORPAY_SECRET"))
        )

        razorpay_order = razorpay_client.order.create(
            dict(amount=amount, currency=currency, payment_capture="0")
        )

        print(razorpay_order)
        razorpay_order_id = razorpay_order["id"]
        status = razorpay_order["status"]
        # status = "created"
        # razorpay_order_id = "12ex213x12"
        if status == "created":
            pay_id = str(uuid.uuid4())[-12:]
            resp = paymentsDb.insert_one(
                {
                    "_id": pay_id,
                    "amount": amount,
                    "razorpay_order_id": razorpay_order_id,
                    "created_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                }
            )
            print(resp)
            appmt_id = str(uuid.uuid4())[-12:]
            user_id = data.get("user_id")
            data = {
                "_id": appmt_id,
                "created_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                "p_name": name,
                "p_mobile": mobile,
                "symptoms": symptoms,
                "spec": spec,
                "payment_id": pay_id,
                "user_id": user_id,
                "completed": False,
                "active": True,
            }
            if doc_id:
                doc_details = doctorsDb.find({"_id": doc_id})
                data["doctor"] = doc_details
            data["razorpay_order_id"] = razorpay_order_id
            print(data)
            consultDb.insert_one(data)
            return JsonResponse({"status": 1, "data": data}, safe=False)
        else:
            return JsonResponse(
                {"status": -1, "msg": "Payment not successful"}, safe=False
            )
    except Exception as err:
        print(str(err))
        return JsonResponse({"status": -1, "msg": "Payment not successful"}, safe=False)


@csrf_exempt
@login_required
def getApmtDetails(request, apmt_id):
    res = list(consultDb.find({"_id": apmt_id}))
    if res:
        return JsonResponse({"data": res[0], "status": 1}, safe=False)
    else:
        return JsonResponse({"status": -1}, safe=False)


@csrf_exempt
def endConsult(request, apmt_id):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        apmt = list(consultDb.find({"_id": apmt_id}))[0]
        duration = data.get("duration")
        tech_ratings = {
            "_id": str(uuid.uuid4())[-12:],
            "video": data.get("video_rating"),
            "audio": data.get("audio_rating"),
        }
        doc_ratings = {
            "doc_id": apmt.get("doctor").get("_id"),
            "user_id": "",
            "rating": data.get("doc_rating"),
            "review": data.get("review"),
        }

        consultDb.update_one(
            {"_id": apmt.get("_id")},
            {
                "$set": {
                    "tech_ratings": tech_ratings,
                    "duration": duration,
                    "complete": True,
                    "active": False,
                }
            },
        )
        ratingsDb.insert_one(doc_ratings)
        return JsonResponse({"status": 1}, safe=False)


@csrf_exempt
@login_required
def currentConsult(request):
    consults = list(consultDb.find({"complete": False}))
    return JsonResponse({"status": 1, "consults": consults}, safe=False)
