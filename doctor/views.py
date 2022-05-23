from pydoc import doc
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import uuid

from healthfit.utils import login_required
from .quadtree.main import Quadtree, Rectangle

# Create your views here.

from healthfit.settings import *

import json
import random as rd

def hee(s, n):
    return s + " "*(n-len(s))

@csrf_exempt
def doctorRegister(request):
    if request.method == "POST":

        # for i in range(73):
        #     data = json.load(open(f"THE_DATA/sample{i}.json"))
        #     print(len(data))
        #     doctorsDb.insert_many(data)

        # doctorsDb.delete_many({})
        # citiesDb.insert_many(data)
        # citiesDb.delete_many({})
        # data = ['Pediatric Dentist', 'Radiologist', 'Podiatrist', 'Internist', 'Physical Therapist', 'Refractive Surgeon', 'Facial Plastic & Reconstructive Surgeon', 'Family Physician', 'Oral Surgeon', 'Family Psychiatric & Mental Health Nurse Practitioner', 'Pain Management Specialist', 'Glaucoma Specialist', 'Hand Surgeon', 'Psychotherapist', 'Geriatrician', 'Physician Assistant', 'Child and Adolescent Psychiatrist', 'Pediatric Emergency Medicine Specialist', 'Laryngologist', 'Nurse Practitioner', 'Plastic Surgeon', 'Dermatologist', 'Pediatric Orthopedic Surgeon', 'Interventional Cardiologist', 'Psychiatrist', 'Endocrinologist', 'Hand & Microsurgery Specialist', 'Ear, Nose & Throat Doctor', 'Emergency Medicine Physician', 'Radiation Oncologist', 'Neuro-Ophthalmologist', 'Colorectal Surgeon', 'Family Nurse Practitioner', 'Chiropractor', 'Nuclear Medicine Specialist', "Women's Health Nurse Practitioner", 'Bariatric Surgeon', 'Spine Specialist', 'Hematologist', 'Prosthodontist', 'Dietitian', 'Infectious Disease Specialist', 'Dentist', 'Pulmonologist', 'Hip and Knee Surgeon', 'Adult Nurse Practitioner', 'Ophthalmologist', 'Midwife', 'Sleep Medicine Specialist', 'Travel Medicine Specialist', 'Periodontist', 'Cardiologist', 'Optometrist', 'OB-GYN', 'Urologist', 'Oculoplastic Surgeon', 'Pediatric / Strabismus Eye Doctor', 'Pediatric Nurse Practitioner', 'Foot & Ankle Specialist', 'Head & Neck Surgeon', 'Pediatric Dermatologist', 'Pediatric Sports Medicine Specialist', 'Primary Care Doctor', 'Forensic Psychiatrist', 'Neurologist', 'Clinical Neurophysiologist', 'Pediatric Cardiologist', 'Addiction Specialist', 'Neuro-Otologist', 'Physiatrist', 'Sinus Surgeon / Rhinologist', 'Surgeon', 'Anesthesiologist', 'Nephrologist', 'Orthopedic Surgeon', 'Psychologist', 'Occupational Therapist', 'Allergist', 'Acupuncturist', 'Vascular Surgeon', 'Sports Medicine Specialist', 'Cornea & External Diseases Specialist', 'Gastroenterologist', 'Rheumatologist', 'Orthodontist', 'Urgent Care Specialist', 'Urological Surgeon', 'Retina Specialist (Medical)', 'Audiologist', 'Nutritionist', 'Adult Psychiatric & Mental Health Nurse Practitioner', 'Diagnostic Radiologist', 'Pediatric Otolaryngologist', 'Neurosurgeon', 'Psychosomatic Medicine Specialist', 'Oncologist', 'Reproductive Endocrinologist', 'Pediatrician', 'Gynecologist', 'Pulmonary Diseases and Critical Care Medicine Specialist', 'Shoulder & Elbow Surgeon', 'Endodontist']

        # d = []
        # for i in data:
        #     r = {
        #         "_id" : str(uuid.uuid4())[-12:],
        #         "specialization" : i
        #     }
        #     d.append(r)
        # specDb.delete_many({})
        # specDb.insert_many(d)
        # citiesDb.delete_many({})
        # doctorsDb.update_many({}, {"$set" : {"user" : "cf00b4ba658c"}})
        # ratingsDb.delete_many({})
        # consultDb.delete_many({})
        all = [doctorsDb, citiesDb, specDb, paymentsDb, usersDb, consultDb, ratingsDb]
        k = {"int" : "Integer", "str" : "String", "dict" : "Object", "float" : "Decimal", "bool" : "Boolean", "NoneType" : "null", "list" : "Array", 'ObjectId' : "String", 'Int64' : "Integer", "datetime" : "Datetime"}
        g = ratingsDb.find_one()
        # print(str(i))
        print()
        for j in g:
            print("\t",hee(j, 20), ": ",hee(k[type(g[j]).__name__], 10))
        print()
        return JsonResponse({})


def getDoctor(requests, doc_id):
    data = list(doctorsDb.find({"_id": doc_id}))[0]
    return JsonResponse(data, safe=False)


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
def searchData(requests):
    if requests.method == "POST":
        data = json.loads(requests.body)
        currPage = data.get("currPage")
        filter = {}
        if not data.get("nearBy"):
            filter["clinic_details.city"] = data.get("city")
        else:
            latitude = data.get("coordinates").get("latitude")
            longitude = data.get("coordinates").get("longitude")
            print(latitude, longitude)
            w = 0.01
            filter["clinic_details.latitude"] = {"$gte" : latitude-w, "$lte" : latitude+w }
            filter["clinic_details.longitude"] = {"$gte" : longitude-w, "$lte" : longitude+w }

        if data.get("spec"):
            filter["main_specialization"] = data.get("spec")
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
        resp = JsonResponse({"cities": d, "specs": a}, safe=False)
        resp["Access-Control-Allow-Headers"] = "*"
        return resp


@csrf_exempt
def addDoctor(request):
    if request.method == "POST":
        print(request.body)
        data = json.loads(request.body)
        appmt_id = data.get("apmt_id")
        doc_id = data.get("doc_id")
        doctor = list(doctorsDb.find({"_id": doc_id}))[0]
        appmt = consultDb.update_one({"_id": appmt_id}, {"$set": {"doctor": doctor}})
        return JsonResponse({"status": 1}, safe=False)


@login_required
def getDashboard(request, doc_id):
    ratings = list(ratingsDb.find({"doc_id": doc_id}))
    consult = list(consultDb.find({"doctor._id": doc_id, "complete": False}))
    return JsonResponse(
        {"status": 1, "ratings": ratings, "consult": consult}, safe=False
    )
