import dataclasses
from django.http import JsonResponse
from django.shortcuts import render
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from healthfit.settings import paymentsDb, consultDb
import uuid
from datetime import datetime
import os
import requests

# Create your views here.

@csrf_exempt
def payments(request):
    data = json.loads(request.body)
    print(data)
    amount = data.get("amount", 0)
    name = data.get("name")
    spec = data.get("spec")
    mobile = data.get("mobile")
    symptoms = data.get("symptoms")
    currency = "INR"
    try:
        razorpay_client = razorpay.Client(
            auth=(os.environ.get('RAZORPAY_KEY_ID'), os.environ.get('RAZORPAY_SECRET')))
        
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))

        print(razorpay_order)
        razorpay_order_id = razorpay_order['id']
        status = razorpay_order['status']
        if status == "created":
            pay_id = str(uuid.uuid4())[-12:]
            resp = paymentsDb.insert_one({
                "_id" : pay_id,
                "amount": amount,
                "razorpay_order_id" : razorpay_order_id,
                "created_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            })
            print(resp)
            appmt_id = str(uuid.uuid4())[-12:]
            user_id = data.get("user_id")
            data = {
                "_id": appmt_id,
                "created_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                "p_name" : name,
                "p_mobile" : mobile,
                "symptoms" : symptoms,
                "spec" : spec,
                "payment_id" : pay_id,
                "user_id" : user_id,
                "complete": False
            }
            data["razorpay_order_id"] = razorpay_order_id
            print(data)
            consultDb.insert_one(data)
            return JsonResponse({"status": 1, "data": data}, safe=False)
        else:
            return JsonResponse({"status": -1, "msg" : "Payment not successful"}, safe=False)
    except Exception as err:
        print(str(err))
        return JsonResponse({"status": -1, "msg" : "Payment not successful"}, safe=False)