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
def payments(request, apmt_id):
    amount = 50000
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
            data = {
                "completed": False,
                "active": True,
            }
            data["razorpay_order_id"    ] = razorpay_order_id
            consultDb.update_one(
                {"_id": apmt_id},
                {
                    "$set": data
                },
            )
            data = consultDb.find({"_id" : apmt_id})
            print(data)
            return JsonResponse({"status": 1, "data": data[0]}, safe=False)
        else:
            return JsonResponse(
                {"status": -1, "msg": "Payment not successful"}, safe=False
            )
    except Exception as err:
        print(str(err))
        return JsonResponse({"status": -1, "msg": "Payment not successful"}, safe=False)

@csrf_exempt
@login_required
def updateConsult(request, apmt_id):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        doc_id = data.get("doc_id")
        if data.get("doc_id"):
            doctor = list(doctorsDb.find({"_id": doc_id}))
            print(doctor)
            if doctor:
                data["doctor"] = doctor[0]
                data.pop("doc_id")
            else:
                return JsonResponse({"status": -1, "msg": "Doctor not found."}, safe=False)
        consultDb.update_one(
            {"_id": apmt_id},
            {
                "$set": data
            },
        )
        data = consultDb.find({"_id" : apmt_id})[0]
        return JsonResponse({"status": 1, "data" : data}, safe=False)
            


@csrf_exempt
@login_required
def getApmtDetails(request, apmt_id):
    print(request.user)
    res = list(consultDb.find({"_id": apmt_id}))
    if res:
        return JsonResponse({"data": res[0], "status": 1}, safe=False)
    else:
        return JsonResponse({"status": -1}, safe=False)

@csrf_exempt
@login_required
def startConsult(request):
    if request.method == "POST":
        appmt_id = str(uuid.uuid4())[-12:]
        data = {
            "_id": appmt_id,
            "created_at": datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        }
        consultDb.insert_one(data)
        return JsonResponse({"status": 1, "data": data}, safe=False)

@csrf_exempt
@login_required
def endConsult(request, apmt_id):
    user = request.user
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        apmt = list(consultDb.find({"_id": apmt_id}))[0]
        duration = data.get("duration")
        tech_ratings = {
            "video": max(1, min(int(data.get("video_rating", 10)), 10), 1),
            "audio": max(1, min(int(data.get("audio_rating", 10)), 10), 1),
        }
        doc_ratings = {
            "_id": str(uuid.uuid4())[-12:],
            "doc_id": apmt.get("doctor").get("_id"),
            "user_id": user.get("_id"),
            "rating": max(1, min(int(data.get("doc_rating", 10)), 10), 1),
            "review": data.get("review"),
        }

        change = {
                    "tech_ratings": tech_ratings,
                    "duration": duration,
                    "completed": True,
                    "end_time" :  datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                }
        if apmt.get("ended_by")==None:
            change["ended_by"] = user


        consultDb.update_one(
            {"_id": apmt.get("_id")},
            {
                "$set": change
            },
        )
        ratingsDb.insert_one(doc_ratings)
        return JsonResponse({"status": 1}, safe=False)


@csrf_exempt
@login_required
def currentConsult(request):
    consults = list(consultDb.find({"complete": False}))
    print(consults)
    return JsonResponse({"status": 1, "consults": consults}, safe=False)

@login_required
def allAppointments(request):
    doc_id = request.GET.get("doc_id")
    user_id = request.GET.get("user_id")
    filter = {}
    if doc_id:
        filter["doctor.user"] = doc_id
    if user_id:
        filter["user_id"] = user_id
    res = list(consultDb.find(filter))
    print(res)
    return JsonResponse({"status" : 1, "data": res}, safe=False)