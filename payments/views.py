from django.http import JsonResponse
from django.shortcuts import render
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from healthfit.settings import paymentsDb
import uuid
from datetime import datetime

# Create your views here.

@csrf_exempt
def payments(requests):
    data = json.loads(requests.body)
    amount = data.get("amount", 0)
    appointment_id = data.get("appointment_id")
    currency = "INR"
    try:
        razorpay_client = razorpay.Client(
            auth=('rzp_test_eCu1qUcpkGwpvc', 'eXTbuwp11dgIwTmcW21sRb5M'))
        
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))

        razorpay_order_id = razorpay_order['id']
        resp = paymentsDb.insert({
            "_id" : str(uuid.uuid4()[-12:]),
            "appointment_id" : appointment_id,
            "amount": amount,
            "razorpay_order_id" : razorpay_order_id,
            "created_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        })
        return JsonResponse({"status": 1, "razorpay_order_id" : razorpay_order_id}, safe=False)
    except Exception as err:
        print(str(err))
        return JsonResponse({"status": -1}, safe=False)