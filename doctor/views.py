from pydoc import doc
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import uuid

from healthfit.utils import login_required, shield
from .quadtree.main import Quadtree, Rectangle

# Create your views here.

from healthfit.settings import *

import json
import random as rd


def hee(s, n):
    return s + " " * (n - len(s))


@csrf_exempt
@shield
def doctorRegister(request):
    d = list(doctorsDb.find({}, {"_id" : 1}))
    for i in d:
        doctorsDb.update_one({"_id" : i["_id"]}, {"$set" : {"active": rd.choice([False, True]), "online": rd.choice([False, True])}})
    return JsonResponse({})


@shield
def getDoctor(requests, doc_id):
    print(doc_id)
    data = list(doctorsDb.find({"$or" : [{"_id": doc_id}, {"user": doc_id}]}))
    print(data)
    if data:
        return JsonResponse({"status": 1, "data": data[0]}, safe=False)
    else:
        return JsonResponse({"status": -1, "msg": "Doctor Not Found"}, safe=False)


def findNearMe(places, latitude, longitude, w=0.006):

    rect = Rectangle(28.500061, 77.012084, 28.750282, 77.371897)
    qt = Quadtree(rect)
    for i in places:
        qt.insert(i["clinic_details"]["latitude"], i["clinic_details"]["longitude"], i)

    range = Rectangle(latitude - w, longitude - w, 2 * w, 2 * w)
    points = []
    qt.nearby(range, points)
    print(len(points), len(places))
    ans = []
    for i in points:
        ans.append(i.id)
    return ans


@csrf_exempt
@shield
def searchData(requests):
    if requests.method == "POST":
        data = json.loads(requests.body)
        currPage = data.get("currPage")
        filter = {}
        if data.get("doc_name"):
            filter["name"] = data.get("doc_name")
        if not data.get("nearBy"):
            if data.get("city"):
                filter["clinic_details.city"] = data.get("city")
        else:
            latitude = data.get("coordinates").get("latitude")
            longitude = data.get("coordinates").get("longitude")
            print(latitude, longitude)
            w = 0.01
            filter["clinic_details.latitude"] = {
                "$gte": latitude - w,
                "$lte": latitude + w,
            }
            filter["clinic_details.longitude"] = {
                "$gte": longitude - w,
                "$lte": longitude + w,
            }

        if data.get("spec"):
            filter["main_specialization"] = data.get("spec")
        if data.get("available"):
            filter["active"] = True
        resp = []
        if filter!={}:
            resp = list(doctorsDb.find(filter))
            rd.shuffle(resp)
            if data.get("sortBy") == "nearest":
                points = findNearMe(resp, latitude, longitude)
        return JsonResponse(list(resp)[10 * (currPage - 1) : 10 * currPage], safe=False)
    else:
        cities = list(citiesDb.find())
        d = []
        for i in cities:
            d.append(i["city"])
        specs = list(specDb.find())
        a = []
        for i in specs:
            a.append(i["specialization"])
        resp = JsonResponse({"status":1, "cities": d, "specs": a}, safe=False)
        resp["Access-Control-Allow-Headers"] = "*"
        return resp


@csrf_exempt
@login_required
@shield
def addDoctor(request):
    if request.method == "POST":
        print(request.body)
        data = json.loads(request.body)
        appmt_id = data.get("apmt_id")
        doc_id = data.get("doc_id")
        doctor = list(doctorsDb.find({"_id": doc_id}))
        if doctor:
            appmt = consultDb.update_one(
                {"_id": appmt_id}, {"$set": {"doctor": doctor[0]}}
            )
            return JsonResponse({"status": 1}, safe=False)
        else:
            return JsonResponse({"status": -1, "msg": "Doctor not found"})


from datetime import datetime


@login_required
@shield
def getDashboard(request, doc_id):
    doctor = checkDoc(doc_id)
    print(doctor)
    if not doctor:
        return JsonResponse({"status": -1, "msg": "Doctor not found."})
    ratings = list(ratingsDb.find({"doc_id": doctor["_id"]}))
    consult = list(consultDb.find({"doctor._id":doctor["_id"], "completed": False}))
    all_ratings = len(ratings)
    all_consult = len(consult)
    positive_reviews = 0
    overall_rating = 0
    positive_reviews_perc = 0
    #overall rating calc
    s = 0
    if all_ratings>0:
        for i in ratings:
            s+=i["rating"]
            if i["rating"]>7:
                positive_reviews+=1
        overall_rating = round(s/all_ratings, 1)
        positive_reviews_perc = (positive_reviews/all_ratings)*100


    res = []
    for i in consult:
        timediff = (
            datetime.now() - datetime.strptime(i["created_at"], "%d/%m/%Y, %H:%M:%S")
        ).total_seconds()
        if timediff < 30 * 60:
            i["current"] = True
            res.append(i)
        else:
            consultDb.update_one({"_id": i["_id"]}, {"$set": {"completed": True}})

    return JsonResponse({"status": 1, "ratings": ratings, "consult": res, "all_ratings":all_ratings, "all_consult":all_consult, "positive_reviews": positive_reviews, "overall_rating": overall_rating, "positive_reviews_perc":positive_reviews_perc}, safe=False)


def checkDoc(doc_id):
    res = doctorsDb.find({"$or" : [{"_id": doc_id}, {"user": doc_id}]})
    if res:
        return res[0]


@login_required
@csrf_exempt
@shield
def updateDocStatus(request, doc_id):
    user = request.user
    if request.method == "POST":
        doc = checkDoc(doc_id)
        if doc:
            if doc.get("user") == user.get("_id"):
                data = json.loads(request.body)
                print(data)
                online = data.get("online", False)
                active = data.get("active", False)
                doctorsDb.update_one(
                    {"_id": doc_id}, {"$set": {"online": online, "active": active}}
                )
                return JsonResponse({"status": 1}, safe=False)
            else:
                return JsonResponse(
                    {"status": 403, "msg": "Not Authorized"}, safe=False
                )
        else:
            return JsonResponse({"status": 404, "msg": "Doctor not found"}, safe=False)


@csrf_exempt
@shield
def getReviews(request, doc_id):
    print(doc_id)
    res = list(ratingsDb.find({"doc_id": doc_id}))
    return JsonResponse({"status": 1, "data": res}, safe=False)


import re


@csrf_exempt
@shield
def getDoctorsByName(request):
    query = request.GET.get("query", "").title()
    search_expr = re.compile(f"^{query}")
    print(query)
    # print(list(doctorsDb.distinct("name")))
    res = []
    if query:
        res = list(doctorNamesDb.find({"name": search_expr}))
    # print(res)
    return JsonResponse({"status": 1, "data": res}, safe=False)
