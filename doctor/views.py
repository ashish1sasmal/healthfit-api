from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import uuid

# Create your views here.

from healthfit.settings import doctorsDb, citiesDb, specDb

import json



@csrf_exempt
def doctorRegister(request):
    if request.method == "POST":

        # for i in range(8):
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
        return JsonResponse({})

def getDoctors(requests):
    data = list(specDb.find().limit(100))
    return JsonResponse(data, safe=False)

@csrf_exempt
def searchData(requests):
    if requests.method == "POST":
        data = json.loads(requests.body)
        resp = doctorsDb.find(
            {
                "clinic_details.city" : data["city"],
                "main_specialization" : data["spec"]
            }
        )
        # print(list(resp))
        return JsonResponse(list(resp)[:20], safe=False)
        
    else:
        cities = list(citiesDb.find())
        d = []
        for i in cities:
            if i["state"] == "New Delhi":
                d.append(i["city"])
        specs = list(specDb.find())
        a = []
        for i in specs:
            a.append(i["specialization"])
        resp = JsonResponse({
            "cities" : d,
            "specs" : a
        }, safe=False)
        resp["Access-Control-Allow-Headers"] = "*"
        return resp