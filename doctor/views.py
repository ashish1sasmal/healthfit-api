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
        # for i in range(73):
        #     data = json.load(open(f"THE_DATA/sample{i}.json"))
        #     print(len(data))
        #     doctorsDb.insert_many(data)

        # doctorsDb.delete_many({})
        # citiesDb.insert_many(data)
        # citiesDb.delete_many({})
        # data = ['Pediatric Dentist', 'Radiologist', 'Podiatrist', 'Internist', 'Physical Therapist', 'Refractive Surgeon', 'Facial Plastic & Reconstructive Surgeon', 'Family Physician', 'Oral Surgeon', 'Family Psychiatric & Mental Health Nurse Practitioner', 'Pain Management Specialist', 'Glaucoma Specialist', 'Hand Surgeon', 'Psychotherapist', 'Geriatrician', 'Physician Assistant', 'Child and Adolescent Psychiatrist', 'Pediatric Emergency Medicine Specialist', 'Laryngologist', 'Nurse Practitioner', 'Plastic Surgeon', 'Dermatologist', 'Pediatric Orthopedic Surgeon', 'Interventional Cardiologist', 'Psychiatrist', 'Endocrinologist', 'Hand & Microsurgery Specialist', 'Ear, Nose & Throat Doctor', 'Emergency Medicine Physician', 'Radiation Oncologist', 'Neuro-Ophthalmologist', 'Colorectal Surgeon', 'Family Nurse Practitioner', 'Chiropractor', 'Nuclear Medicine Specialist', "Women's Health Nurse Practitioner", 'Bariatric Surgeon', 'Spine Specialist', 'Hematologist', 'Prosthodontist', 'Dietitian', 'Infectious Disease Specialist', 'Dentist', 'Pulmonologist', 'Hip and Knee Surgeon', 'Adult Nurse Practitioner', 'Ophthalmologist', 'Midwife', 'Sleep Medicine Specialist', 'Travel Medicine Specialist', 'Periodontist', 'Cardiologist', 'Optometrist', 'OB-GYN', 'Urologist', 'Oculoplastic Surgeon', 'Pediatric / Strabismus Eye Doctor', 'Pediatric Nurse Practitioner', 'Foot & Ankle Specialist', 'Head & Neck Surgeon', 'Pediatric Dermatologist', 'Pediatric Sports Medicine Specialist', 'Primary Care Doctor', 'Forensic Psychiatrist', 'Neurologist', 'Clinical Neurophysiologist', 'Pediatric Cardiologist', 'Addiction Specialist', 'Neuro-Otologist', 'Physiatrist', 'Sinus Surgeon / Rhinologist', 'Surgeon', 'Anesthesiologist', 'Nephrologist', 'Orthopedic Surgeon', 'Psychologist', 'Occupational Therapist', 'Allergist', 'Acupuncturist', 'Vascular Surgeon', 'Sports Medicine Specialist', 'Cornea & External Diseases Specialist', 'Gastroenterologist', 'Rheumatologist', 'Orthodontist', 'Urgent Care Specialist', 'Urological Surgeon', 'Retina Specialist (Medical)', 'Audiologist', 'Nutritionist', 'Adult Psychiatric & Mental Health Nurse Practitioner', 'Diagnostic Radiologist', 'Pediatric Otolaryngologist', 'Neurosurgeon', 'Psychosomatic Medicine Specialist', 'Oncologist', 'Reproductive Endocrinologist', 'Pediatrician', 'Gynecologist', 'Pulmonary Diseases and Critical Care Medicine Specialist', 'Shoulder & Elbow Surgeon', 'Endodontist']

        # rev = ["The services that I receive from (DN) is excellent. Dr. (Name) and the staff are friendly and ensure that I am properly informed about my health and care. I would have no qualms in recommending them to friendly and friends.","Dr. (Name) did a great job with my first ever health exam. She explained everything to me in a very clear manner. She was also kind and friendly. All of the staff was great – they were helpful, patient and helped with my insurance.","Wonderful experience with (Clinic name). Dr. (Name) was a wonderful surgeon, and the staff was always helpful and kind. They ensured I had a smooth prep, surgery, and follow-up. I am so glad I chose (Clinic name) and would highly recommend to anyone.","Dr. (Name) is incredible. Not only has she taken great care of my health, but also she is lovely to speak with at every appointment. It’s rare to find a doctor that combines such personal touches and care for a patient as a person with outstanding quality of medical care. I highly recommend becoming her patient!","Great medical office, wonderful and warm experience from start to finish. Appreciate Dr. (Name) taking time to go over the diagnosis clearly and treatment options. Was referred over by my general doctor and can see why. Highly recommended.","Great experience as a first timer. I barely waited to be helped when I checked in. The staff and Dr. (Name) were all very friendly and helpful. I especially loved how Dr. (Name) really took his time to explain my conditions with me as well as my treatment options. I had a great visit and the doctor’s demeanor has really put me at ease so I highly recommend this clinic.","Dr. (Name) gets it. From his excellent treatment, curiosity, investigative mind and ability to connect, you know where you stand immediately and what next steps look like. Attention doctors if you want a masterclass in watching a doctor bring medical knowledge and build rapport so that message is heard by patient and therefore delivered watch this guy.","This practice is terrific. Dr. (Name) combines expertise and a willingness to listen and discuss. She’s also an excellent surgeon. Also, the staff is very friendly and professional. I’ve never had to wait more than a few minutes when I arrive on time for an appointment.","Dr. (Name) was terrific. Knowledgeable, sensitive, informative… I immediately felt at ease – and felt confident in my receiving expert medical care. Staff was great, too. Walked away, very impressed w. the overall experience. HIGHLY recommend.","Dr. (Name) is a great doctor! He’s very understanding and listens to your concerns. He takes time with the patient to help them with their health issues! I highly recommend him to anyone looking for a specialist.","Great experience! Made a same day appointment on (Clinic name) and got in right away. The front desk staff and the medical assistant were very nice and helpful. Dr. (Name) was great, gave realistic expectations and timelines. I will definitely be back and would recommend the practice!","Dr. (Name) is extremely professional: he takes time to listen and time to explain. A first rate professional experience. Completely satisfied with Dr. (Name) and all the support staff.","Really thorough, detailed care. Dr. (Name) cares about his patients and even gave me a free visit when I complained of post-op pain and I was transitioning between insurances.","Dr. (Name) and the entire staff at (Clinic name) are beyond amazing. When you have an appointment, they will spend the whole scheduled period with you if need be; I know when I come in to see Dr. (Name), he’s already reviewed the reasons for my coming in and my file. I never feel rushed, and he always asks if I have any other questions. He’s awesome. Also, when he knew my medication was expensive on my insurance, he looked up what competing pharmacies charged with GoodRX and printed me out the prices – saved me lots!","Dr. (Name) is great. He has been very attentive to my health issues. I have had complicated health problems and he has addressed them all. He is very kind and patient. I am very grateful for him.","Dr. (Name) has been really professional and has shown true commitment to solve my health issues. We are still addressing them, but he has made me feel I’m in good hands.","Dr. (Name) is the best! Each time we have met, she has provided thorough examinations and has shown genuine concern. I’ve had nothing but great encounters with her.","Dr. (Name) is our favorite Medical provider. She is always friendly, thoughtful, and puts our concerns first. I can not speak more highly of her. The staff is always helpful and my experience with other medical professionals in this office has always been above my level of standards.","I recently had my first visit with Dr. (Name) and it was a delight. She immediately made me feel very comfortable and it felt as if she had been my doctor for years. I am very happy to have found a primary care physician that I feel I can trust and connect with.","It took me a while to find a doctor that made me feel comfortable and welcome! Dr. (Name) as well as her staff are awesome, they listen and give the best advice. Dr. (Name) really strives to give the best care possible to each of her patients."]

        user = ["d606561ceee4", "0dbf6500002d", "e8746781d88c", "77d0bc19b997", "6e4ba5da1373", "7266060e26e1", "b32ae5bed50c", "f0a3561219fa" ]

        # for i in user:
        #     u = list(usersDb.find({"_id" : i}))[0]
        #     ratingsDb.update_many({"user_id" : i}, {"$set":{"user_name" : u["full_name"]}})
        # l = set()
        # for i in data:
        #     r = doctorsDb.find({"main_specialization" : i})
        #     for j in r[:30]:
        #         for x in range(rd.randint(1, 6)):
        #             ratingsDb.insert_one({
        #                 "_id" : str(uuid.uuid4())[-12:],
        #                 "doc_id" : j["_id"],
        #                 "user_id" : rd.choice(user),
        #                 "rating" : rd.randint(4, 11),
        #                 "review" : rd.choice(rev)
        #             })
                # l.add(j["_id"])
        # print(l)

        # d = ['Abagael Dumbrell', 'Abbe Aronin', 'Abbie Demageard', 'Abelard Norsister', 'Abner Pieter', 'Adam Darmody', 'Adam Mc Elory', 'Adams Frammingham', 'Adelheid Dutch', 'Adelina Martinon', 'Adey Downer', 'Adolf Overstreet', 'Adolf Shinton', 'Aggi Kinvan', 'Agnella Cattellion', 'Agnella Deacon', 'Agnes Copestake', 'Ahmad Deely', 'Ailbert Zoellner', 'Aileen Loveredge', 'Al Bartomeu', 'Alano Tinsley', 'Alanson Akett', 'Alberta Baudin', 'Aldin Paff', 'Alejandrina Harman', 'Alejandro Alibone', 'Alfonso MacDermand', 'Alick Du Fray', 'Alick Harwin', 'Aline Caslett', 'Alis Springford', 'Alix Bidwell', 'Allard Hounson', 'Allen Hayley', 'Alley Tomeo', 'Alli MacEllen', 'Allis Heare', 'Allister Siman', 'Allys Bwy', 'Allys Skelbeck', 'Almeda Groves', 'Almeda Hardage', 'Alonzo Kuhnt', 'Aluino Boyne', 'Aluino Bullard', 'Alverta Chaperling', 'Alyce Sabie', 'Amandie McGrayle', 'Ambrosius Goundsy', 'Amy Roche', 'Anders Tufts', 'Andi Mullineux', 'Andrey Minto', 'Andriette Klimpt', 'Angelique Chance', 'Angelle Swinfen', 'Angy McBeith', 'Anita Sambiedge', 'Ann Dimmock', 'Annaliese Polotti', 'Annecorinne Romeuf', 'Anni Lismer', 'Ansel Roches', 'Antin Marskell', 'Anton McGurgan', 'Antonia Geroldini', 'Any Davion', 'Arabel Offell', 'Archaimbaud Ainsley', 'Ardenia Dawbery', 'Ardisj Pessolt', 'Ardra Vescovo', 'Arlen Stormont', 'Arlin Ockwell', 'Arlin Raigatt', 'Arlina Scoates', 'Armstrong Jacquemet', 'Arnold Skayman', 'Aron Rickson', 'Artemis Rappa', 'Arthur Carlaw', 'Arthur Reeme', 'Arv Bradick', 'Arvy Ball', 'Ashbey Catcheside', 'Ashlie Purviss', 'Auberon Swannell', 'Audrie Paddon', 'Audrye Woodruff', 'Aurea Stooke', 'Avery Wofenden', 'Avram Leavold', 'Avril Mouser', 'Ax Kyrkeman', 'Axe Shard', 'Bailie Rhoddie', 'Baillie Cornelisse', 'Baird Allum', 'Balduin Carlow', 'Bancroft Broun', 'Bar Matyashev', 'Barbie McCreath', 'Bard Brunn', 'Barnard Batterbee', 'Barris Dalston', 'Barris McElmurray', 'Bartlett Halfacree', 'Bartolemo Siggins', 'Basile Berthod', 'Bax Sulman', 'Bekki Brightwell', 'Bekki McInerney', 'Belicia Cowmeadow', 'Bellanca Squirrell', 'Benedikt Jacobowits', 'Benton Brokenshaw', 'Berkly Landreth', 'Bernadina MacRedmond', 'Bernita Mum', 'Berny MacDunlevy', 'Bertha Pressnell', 'Beryl Raoult', 'Bessy Brodley', 'Betta August', 'Betteanne Forgie', 'Bev Jacobbe', 'Beverlee Hawking', 'Beverly Avrahamian', 'Bill Bamborough', 'Billy Malster', 'Blanche Allbut', 'Blane McCrachen', 'Blayne Warder', 'Blondell Aronstein', 'Bobbee Dando', 'Bobette Wemyss', 'Bond Winfield', 'Bondon Noorwood', 'Brand Brunstan', 'Brandice Baglow', 'Bree Huffer', 'Brendan Sacase', 'Brian Sanderson', 'Britte Seneschal', 'Brocky Flory', 'Bron Bicheno', 'Bronnie Morrallee', 'Bronny Sabathe', 'Bunnie Cund', 'Bunny Skippen', 'Butch Yorke', 'Byram Oldridge', 'Byrom Mighele', 'Calida Hairsnape', 'Calv Sofe', 'Candie Hugo', 'Caralie Korneichuk', 'Carina Botton', 'Carla Kneeshaw', 'Carlie Barnwill', 'Carlita Deards', 'Carlita Lillywhite', 'Carma Starmont', 'Carmelia Drinan', 'Carmelita Flaverty', 'Carmencita Wharram', 'Carmine Bradman', 'Carol Houseago', 'Carolann Lafond', 'Carri Hulburt', 'Carrissa Astlet', 'Carrissa Fairfull', 'Carrissa Minall', 'Casar Kilty', 'Casi Craythorne', 'Cassaundra Alpe', 'Cassaundra Soppit', 'Cassie Amthor', 'Catriona MacCurlye', 'Cecilio Copplestone', 'Cecily Fain', 'Cedric Gustus', 'Celina Tait', 'Celinda Broune', 'Chalmers Potte', 'Chandra Norway', 'Charla Feilden', 'Charla Laxton', 'Charla McCurtin', 'Charlotte Ellam', 'Charmian Vidgen', "Charo O' Gara", 'Chase Loveday', 'Cherilynn Felton', 'Chickie Keetley', 'Chico Appleyard', 'Chlo Kinver', 'Chloe Applin', 'Chloe Looks', 'Chris Cheng', 'Chris Cicco', 'Christabel Crippill', 'Christan Sowman', 'Christie Blencowe', 'Christoph Morteo', 'Cicily Brabbs', 'Ciro Bestiman', "Clair O' Bee", 'Claudina Norvel', 'Claudius Doles', 'Claus Kropp', 'Claus Parnaby', 'Cletis Karpinski', 'Cleve Goeff', 'Cobbie Duffill', "Codi O'Lyhane", 'Colas Durand', 'Collete Hattrick', 'Colver Wilprecht', 'Conan Yokley', 'Conrad Streeter', 'Coralyn Howselee', 'Coralyn Zambonini', 'Coreen MacCleod', 'Corella Lingfoot', 'Corny Ockendon', 'Correy Chasmor', 'Corrie Shutler', 'Corry Spray', 'Cortney Broggelli', 'Cory Robbins', 'Cosetta Lambis', 'Courtenay Tourne', 'Cozmo Fores', 'Cristie Willeson', 'Cullan Quakley', 'Cyndy Rolland', 'Cynthia Champness', 'Cynthia McChesney', 'Cynthy Life', 'Daffie Fairnington', 'Daffy Lancaster', 'Daisy Blade', 'Dalis Krugmann', 'Dallon Brownill', 'Damien Moughtin', "Dana O'Cooney", 'Danice Ranken', 'Daniele Cypler', 'Danit Chauvey', 'Danita Plumb', 'Danyelle Lob', 'Danyette Stanyon', 'Darcie Bridie', 'Darelle Skillings', 'Dari Dewire', 'Darleen Mutton', 'Darrel Simpole', 'Dave Yanov', 'Davidson Kernes', 'Dean Dace', 'Dede Hallitt', 'Dee dee Brotherick', 'Dehlia Bartalucci', 'Delcina Baccus', 'Delcine Fenech', 'Delphinia Shirtcliffe', 'Demetris Ebunoluwa', 'Dene Ginger', 'Deni Ferriby', 'Derek McMorran', 'Derrek Bagehot', 'Desiri Pethybridge', 'Desmond Pepon', 'Devora Abramovici', 'Devora Branscombe', 'Dianna Ambroisin', 'Dianne Lutas', 'Dicky Regorz', 'Dina Aubrey', 'Dionne Braisher', 'Dolf Allinson', 'Dolph Emmet', 'Donaugh Harries', 'Donetta Deadman', 'Doralin Cawthra', 'Dore Harcase', 'Dorella Meert', 'Dorella Woolford', 'Dorie Minshull', 'Dorisa Boobier', 'Dredi Heady', 'Dru Scranedge', 'Drucie Croal', 'Dulcy Mangin', "Dun D'Almeida", 'Durante Iggalden', 'Dwight Lowsely', 'Ebba Cheke', 'Eda Sauvage', 'Eddie Duce', 'Edin MacCleay', 'Editha Tull', 'Edlin Horder', 'Eirena Pinkerton', 'Elden Metzke', 'Elena Dunton', 'Elena Everix', 'Eleni Mechic', 'Eleonora Cahani', 'Elfreda Tratton', 'Elga Marriot', 'Elizabeth Alster', 'Ellary Winspare', 'Ellen Heady', 'Ellerey Feek', 'Ellery Hallut', 'Elli Brooksbie', 'Elora Barras', 'Elroy Cowan', 'Elston Coldman', 'Elysee MacCrackan', 'Elysia Mirralls', 'Emelia Cockill', 'Emylee Dimitriev', 'Englebert Franzonello', 'Enrica Swainsbury', 'Eran Ferrillo', 'Erasmus Grabban', 'Erich Florey', 'Ernestine Care', 'Ernie Paynton', "Errol M'Quharge", 'Esteban Robberecht', 'Estevan Letteresse', 'Esther Bowmer', 'Esther Wadwell', 'Etheline Brigginshaw', 'Eugenie Secombe', 'Eva Dellar', 'Evaleen Grishakin', 'Evangelia Pithcock', 'Evie Peers', 'Fairfax Ricardo', 'Far Hackin', 'Faythe Greensall', 'Felic McCrone', 'Felike Chippindall', 'Felike Swansbury', 'Felita Oakenfield', 'Ferguson Higginbottam', 'Fielding Dasent', 'Fifi Campanelli', 'Fifine Dubble', 'Filide Kitman', 'Finley Maple', 'Fiona Frere', 'Fionnula Okill', 'Fitzgerald Yorston', 'Flinn Hassell', 'Flor Cromie', 'Florentia Cristofolini', 'Florrie Thornally', 'Floyd Iliffe', 'Forbes Seman', 'Francene Studders', 'Franni Desson', 'Franzen Kenworthey', 'Fraser Hinrich', 'Frazier Giannoni', 'Frederique McCaskell', 'Friederike Fleeman', 'Friedrich Deners', 'Gabrila Goose', 'Gabrila Noir', 'Gail Fattorini', 'Galven Guitt', 'Gannie Fakes', 'Gard Yakovich', 'Gardie Boswood', 'Garey Marlow', 'Garrick Spence', 'Garv Babe', 'Garv Kennicott', 'Garvey Mustill', 'Gay Mollen', 'Geneva Degoy', 'Genna Speares', 'Geordie Tunno', 'George Gaul', 'Geraldine Stopford', 'Gertruda Hubberstey', 'Gibb Yepiskopov', 'Gilbertine Droghan', 'Gilles Zorn', 'Gilli Gater', 'Giorgi Nozzolii', 'Giovanni Dmitriev', 'Giovanni Lemmen', 'Gipsy Marl', 'Giraldo De Zamudio', 'Giulio Cromie', 'Glad Atkinson', 'Glenna Kobes', 'Goddard Lydiatt', 'Goober Bramsen', 'Grantley Dilley', 'Gretel Pedlingham', 'Grissel Ramelet', 'Guinna Malley', 'Gun Perigoe', 'Gus Kyncl', 'Gus Livingstone', 'Gussi Kermit', 'Gusta Seid', 'Guy Mullineux', 'Gwen Iacopo', 'Gweneth Mc Andrew', 'Hadria Spofforth', 'Haley Pountain', 'Halley Vreiberg', 'Halli Cullip', 'Halsy Harkus', 'Happy Brunelleschi', 'Harli Quantick', 'Harmony Jobb', 'Haslett Shanahan', 'Hasty Beamond', 'Hatty Ridder', 'Haze Nestor', 'Heidie Lewinton', 'Helaina Castillo', 'Helaina Noli', 'Hendrik Marcq', 'Henriette Marchelli', 'Hephzibah Thurlow', 'Herby Mougeot', 'Heriberto Rayson', 'Hermina Eggins', 'Hermon Tanner', 'Herta Silburn', 'Herve Kellington', 'Hestia Gierhard', 'Hewe Cavie', 'Hilarius Greatham', 'Hilary Chapple', 'Hildy Roles', 'Hillard Smale', 'Hillyer Pettyfer', 'Hollis Lifton', 'Holly Grcic', 'Holly Gwatkin', 'Holly-anne Baigrie', 'Horatia Ingerfield', 'Horatio Ault', 'Humbert Fontell', 'Hymie Conklin', 'Iain Keates', 'Ibbie Althorpe', 'Ilaire Sandiford', 'Ilene Sommerscales', 'Illa Haith', 'Ingar Scully', 'Inger Marcussen', 'Inglis Gaine of England', 'Innis Middle', 'Isaac Gommery', 'Isabella Lyles', 'Isac Probyn', 'Isidora Scolts', 'Issiah Ashfold', 'Ivonne Pechell', 'Jabez Calcut', 'Jacenta Lyvon', 'Jacki Rockliffe', 'Jacob Klemensiewicz', 'Jada Genever', 'Jaine MacCarrane', 'Jamie Dutton', 'Janaya Batts', 'Janean Brien', 'Janella Stollhofer', 'Janene De Courtney', 'Jareb Farley', 'Jarred Wesgate', 'Jarrod Toyer', 'Jaymie Bohin', 'Jaynell Dzenisenka', 'Jeana Sahnow', 'Jedd Charleston', 'Jenilee Capron', 'Jens Labden', 'Jeremy Iacapucci', 'Jermain Emeney', 'Jerrie Waliszewski', 'Jerrome Prue', 'Jess De Few', 'Jess Penrose', 'Jeth Matterson', 'Jill Mayou', 'Jinny Brech', 'Jo Alcalde', 'Joannes Stodit', 'Jobye Holtum', 'Jodie Beedle', 'Joela Hackney', 'Joella Berndt', 'Joete Clohessy', 'Joey Longwood', 'Johnath Babber', 'Johnath Leuren', 'Joni Epine', 'Jordan Binden', 'Jordan McIlvoray', 'Jori Borzone', 'Josey Philipps', 'Joshuah Hambleton', 'Joyann Prott', 'Juanita Izkovicz', 'Judd Franceschino', 'Julee Merrell', 'Juline Masding', 'Junette Braun', 'Junia Habard', 'Justen Patnelli', 'Justen Winspur', 'Justin McAnulty', 'Kacey Ketch', 'Kaitlin Mowle', 'Kaja Lehrer', 'Kala Kolodziej', 'Kaleena Leavry', 'Kariotta Danell', 'Karolina Anscombe', 'Karrah Binge', 'Kary Buntain', 'Katey Gauge', 'Katey Nafziger', 'Kaylil Card', 'Kean Heart', 'Keefe Uwins', 'Keelby Enoch', "Keene O'Gavin", 'Kelcie Brockhurst', 'Kellia Burfitt', 'Kellia Seear', 'Kelly Duberry', 'Kenn Keningham', 'Keri Wannell', 'Kerrin Thal', 'Kerry Corderoy', 'Kevyn Phipson', "Ki O' Timony", 'Kiah Chasen', 'Kiele MacElharge', 'Killian Ogborne', 'Killie Lie', 'Kimmie Crampsey', 'Kimmie Pencost', 'Kirk Everist', 'Korella Reville', 'Korry Fetter', 'Kort Ridgley', 'Kristopher Thornhill', 'L;urette Forty', 'Lanie McArtan', 'Larissa Flitcroft', 'Lauree Cicchelli', 'Laureen Fletcher', 'Laurel McSherry', 'Laurene Instone', 'Lavinia Gillon', 'Lavinia Von Welldun', 'Lavinie Levene', 'Lawton Skyrme', 'Lazaro Bilyard', 'Leann Bidmead', 'Lebbie Bloggett', 'Leese Scourge', 'Leigh Oxe', 'Leigh Truran', 'Lelia Alvares', 'Lena Stopp', 'Lenore Gorner', 'Leonidas Oki', 'Leroi Wikey', 'Letta Beevers', 'Levy Campana', 'Lexine Shailer', 'Lexis Mountjoy', 'Libbie McGahy', 'Lidia Orwin', 'Lilith Bonelle', 'Lindsay Libreros', 'Link Erbe', 'Linnell Pellew', 'Linnell Tortice', 'Lise Perford', 'Lissi Uridge', 'Liuka Sanday', 'Liv Czadla', 'Llewellyn Tomaszczyk', 'Locke Devereux', 'Lolly Cubbini', 'Lora Ferretti', 'Lorain Kryska', 'Lotte Staley', 'Louisette Fortin', 'Loutitia Reiglar', 'Lowrance Gradly', 'Luciana Caile', 'Lukas Ferras', 'Lurline Blankley', 'Ly Goodread', 'Lyle Cumbes', 'Lynda Fillgate', 'Lyndy Petz', 'Lynn Calcraft', 'Mabel MacNish', 'Mack Carbett', 'Mackenzie Schermick', 'Madel Dutch', 'Magda Ivanyutin', 'Mahala Rocks', 'Maisey Wildblood', 'Maitilde Duiged', 'Maitilde Fabry', 'Maitilde Yeld', 'Mala Taile', 'Mallory Birwhistle', 'Mandi Brookes', 'Mandi Goldie', 'Mara Vergo', 'Marcel Collington', 'Marcelle Elis', 'Marcellus McKinnell', 'Marchelle Dalzell', 'Marci Hanford', 'Maren Dwane', 'Maren Gealy', 'Maressa Coucher', 'Maria Polding', 'Marian Avarne', 'Mariquilla Guerre', 'Marj McMonnies', 'Marlow Noyes', 'Marshal Braunter', 'Marshal Fricker', 'Marsiella Cushelly', 'Marsiella Simic', 'Martina Grieswood', 'Maryanna Cardenosa', 'Matteo Hukin', 'Matthias Rame', 'Matty Hardington', 'Maude Rattenbury', 'Maure Nunson', 'Maurene Honacker', 'Max Deedes', 'Mayor Stert', 'Megan Cockerill', 'Meghan Baversor', 'Melisse Barthod', 'Melvin Markwell', 'Melvyn Quincee', 'Mercedes Miere', 'Mercy Bane', 'Merissa Ida', 'Merrill Boch', 'Micah Hendricks', 'Mildrid Brahms', 'Milicent Fawdrie', 'Millard Shadbolt', 'Milli Maccari', 'Miltie Woodhouse', 'Minetta Euplate', 'Minni Kenvin', 'Minta Tant', 'Mirabel Commucci', 'Mirabella Dobie', 'Mirella Kilcoyne', 'Miriam Robilart', 'Mirna Antonoczyk', 'Modesty Richten', 'Moe Harrild', "Moe O' Brian", 'Molly Barwack', 'Monah Swinburne', 'Montague Drakard', 'Morgana Extance', 'Mufinella Verrill', 'Murry Ewert', 'Murry Turnock', 'Murvyn Sowden', 'My Saltsberg', 'Mylo Baskerfield', 'Myrle Klaff', 'Myrtle Collip', 'Nancy Langsdon', 'Nanette Ivanishev', 'Nannette Bilbrooke', 'Nara Jefferd', 'Natala Gronaver', 'Nataniel Lapere', 'Nataniel Mityakov', 'Natasha Mixture', 'Nate Lillford', 'Nathalie Charrier', 'Neal Bubeer', 'Nealon Karpol', 'Neda Toye', 'Neddie Lisciandro', 'Neely Elt', 'Neila Vickars', 'Nero Binley', 'Nessie Munslow', 'Nevin Booker', 'Nevins Daynter', 'Neysa Gauler', 'Nial Lochran', 'Nial Veillard', 'Nichols Krolman', 'Nicky Fellenor', 'Nicolais Spinozzi', 'Nicolle Stoakes', 'Nigel Keggin', 'Nikolaus Vynall', 'Noak Hassan', 'Noam Earles', 'Nobie Goreway', 'Noby Barkly', 'Noellyn Plover', 'Norbert McAirt', 'Norby Larder', 'Normie Capstack', 'Norrie Illwell', 'Obidiah Feechan', 'Ode Volke', 'Olia Thinn', 'Oliviero Merwood', 'Olwen Malthouse', 'Omero Heake', 'Oralla Kinnar', 'Orlan Petters', 'Othelia Beston', 'Othelia Yaakov', 'Othilie Guymer', 'Otho Ollerearnshaw', 'Pablo Crapper', 'Paddie Tallon', 'Pamela Trickey', 'Paolina Broad', 'Paolina Cherm', 'Paolo Cubbinelli', 'Park Enstone', 'Parnell Oty', 'Patricio Veneur', 'Patrizia Kenelin', 'Patton Batman', 'Paulo McGoon', 'Pen Rudolfer', 'Penn Ralston', 'Percival Slesser', 'Pernell Dumbellow', 'Peter Stanyland', 'Petr Beefon', 'Petronille Droghan', 'Phedra Caldes', 'Phil Hellis', 'Philis Engelmann', 'Philly Pollak', 'Pierre Checklin', 'Pippo Streets', 'Pollyanna Brittain', 'Prudi Bodsworth', 'Pryce Blaber', 'Puff Emmet', 'Quent Diament', 'Quincey Leece', 'Quincy Hutt', 'Rafaello Izard', 'Rafi Ciepluch', 'Ralph Proschek', 'Rand McIlhone', 'Raphaela Renault', 'Ravi Alvin', 'Raynell Kivlehan', 'Rayshell Antonellini', 'Rayshell Millyard', 'Rebecka Shiels', 'Rebekkah Balnaves', 'Red Vedishchev', 'Reeba Caesar', 'Regen Pakes', 'Renell Jeram', 'Reube Summerson', 'Revkah Bartholomieu', 'Rhetta Skeats', 'Rhiamon Sooper', 'Ricca Vail', 'Ring Le Guin', 'Ripley Bennallck', 'Roanna Bulteel', 'Roanne Pavlitschek', 'Robbi Pobjay', 'Roberto Fremantle', 'Robinson Fidler', 'Rochella Lamartine', 'Roderich Dron', 'Rodolfo MacSkeaghan', 'Roley Le Floch', 'Rollo Westcarr', 'Roman Roller', 'Romonda Bernholt', 'Ronica Sheerman', 'Rosalia Keneford', 'Rosalynd Barnewelle', 'Roseline Newcome', 'Rosella McAusland', 'Rowan Marwood', 'Roxanna Zavattari', 'Rozalin Zwicker', 'Rubetta MacDunleavy', 'Rubie Belfit', 'Ruddy Scroggie', 'Rufus Tombs', 'Ruperto Bowsher', 'Russ Ghione', 'Russ Kedwell', 'Sada Page', 'Salem Ottewell', 'Salomi Podmore', 'Salvador Ingerman', 'Sam Teasey', 'Sammy Petrasch', 'Samson Filson', 'Samuel Ohm', 'Sanders Lamplugh', 'Sandro Dmitriev', 'Sara-ann Bohl', 'Saraann Woodwing', 'Sarina Barniss', 'Sarine Brinsden', 'Saunders Preon', 'Saunderson Beall', 'Saundra Gomer', 'Sax Peck', 'Sayres Cosgriff', 'Seana Hanes', 'Sergeant Burder', 'Sergent Izkoveski', 'Sergio Slocum', 'Shalna Bumby', 'Shandy Guihen', 'Shandy Lorand', 'Shane Rearie', 'Shani Gianulli', 'Sharl Massow', 'Sharleen Rizon', 'Shawna Grzegorczyk', 'Shay Daniello', 'Shay Fechnie', 'Shay Romanet', 'Shaylyn Merington', 'Sheelah Labba', 'Sheilakathryn Dale', 'Shelly Abisetti', 'Sherlocke Tower', 'Sherri Tapin', 'Shurwood Everex', 'Sibilla Perigoe', 'Sig Fierro', 'Silvain Buffery', 'Simmonds Gillatt', 'Sindee Lownie', 'Spencer Barnson', 'Stacie Tesche', 'Starlin Sustin', 'Steffi McCullock', 'Steward Oughton', 'Storm Spires', 'Stormy Leyninye', 'Susan Tregent', 'Susanetta Grunbaum', 'Susanetta Hartzenberg', 'Susanne Moysey', 'Susy Berrygun', 'Suzy Mawby', 'Sybille Parsand', 'Sydel Mouat', 'Tad Sproat', 'Tadio Maddra', 'Tamqrah Lechmere', 'Tan Kattenhorn', 'Tandie Mundall', 'Tanitansy Wyborn', 'Tarrah Reddy', 'Teodoro Porcas', 'Teresa Houseago', 'Terese Axcel', 'Teriann Booley', 'Terrye McQuaide', 'Terrye Rouf', 'Thatch Gauld', 'Thea Gimblett', 'Theodora Macellar', 'Thia Geffcock', 'Thibaut Pepin', 'Thorny Ameer-Beg', 'Thorny Liebmann', 'Thorsten Vaan', 'Tildi Fearns', 'Tiler Norcutt', 'Tiphani Vaen', 'Tish Krzyzowski', 'Tobe Kellitt', 'Tobie Ahrendsen', 'Toinette Hullin', 'Tonie Mechem', 'Tonnie Congreve', 'Tony Filipic', 'Torey Rosenzwig', 'Traci MacPhail', 'Tracie Morter', 'Tremain Petzolt', 'Tremain Tretwell', 'Trescha Staples', 'Tris Vidgen', 'Trstram Girkins', 'Trudey McLellan', 'Tull Medmore', 'Tyler Paskerful', 'Ulick Cheshire', 'Ulises Hamblin', 'Ulrick Shead', 'Ulrika De Giorgis', 'Urban Dannohl', 'Uriel Poure', 'Uta Marcoolyn', 'Uta Zelley', 'Vaclav Moorey', 'Valdemar Hinkens', 'Valenka Dailey', 'Valentine Wisedale', 'Valeria Kuschke', 'Valle Saffrin', 'Vanda Learmont', 'Vassili Renackowna', 'Vassily Staneland', 'Verena Guyet', 'Victor Peare', 'Vinita Aickin', 'Vivianne Dunmore', 'Wade Youthed', 'Walker Berrisford', 'Walther Armatidge', 'Ward Abdie', 'Warren Lawrance', 'Warren Teasdale', 'Welsh Northleigh', 'Wendie Janaszkiewicz', 'Wernher Dollar', 'Westbrook Casellas', 'Whit Reece', 'Wiley Shearwood', 'Willetta Josh', 'Willi Otley', 'Willi Towsie', 'Willie Kilmister', 'Wilmar Quartermain', 'Wilow Enrrico', 'Winn Frane', 'Winne Stainburn', 'Winni Lucock', 'Winnie Blainey', 'Winslow Gaythorpe', 'Woodman Fayne', 'Worth Fairburne', 'Wright Walstow', 'Wynn Lias', 'Wynne Dufore', 'Xena Straw', 'Yancey Hick', 'Yankee Primrose', 'Yolande Meininking', 'Yorgos Kilgrove', 'Yul Du Fray', 'Yulma Matushevich', 'Zachary Southgate', 'Zachery Passby', 'Zarah Yokelman', 'Zared Baynham', 'Zebedee Monery', 'Zebulen Dorking', 'Zed Gahan', 'Zedekiah Eliez', 'Zelma Fooks', 'Zolly Deinhardt', 'Zuzana McMahon']
        c = 0
        # for i in d:
        #     doctorNamesDb.insert_one({"_id" : c, "name" : i})
        #     c+=1


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
        # all = [doctorsDb, citiesDb, specDb, paymentsDb, usersDb, consultDb, ratingsDb]
        # k = {"int" : "Integer", "str" : "String", "dict" : "Object", "float" : "Decimal", "bool" : "Boolean", "NoneType" : "null", "list" : "Array", 'ObjectId' : "String", 'Int64' : "Integer", "datetime" : "Datetime"}
        # g = ratingsDb.find_one()
        # # print(str(i))
        # print()
        # for j in g:
        #     print("\t",hee(j, 20), ": ",hee(k[type(g[j]).__name__], 10))
        # print()
        # doctorsDb.update_many({}, {"$set" : {"online" : False, "active" : True}})
        return JsonResponse({})


def getDoctor(requests, doc_id):
    print(doc_id)
    data = list(doctorsDb.find({"_id": doc_id}))
    print(data)
    if data:
        return JsonResponse({"status" : 1, "data":data[0]}, safe=False)
    else:
        return JsonResponse({"status" : -1, "msg":"Doctor Not Found"}, safe=False)


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
        print(data)
        currPage = data.get("currPage")
        filter = {}
        print(data)
        if data.get("doc_name"):
            filter["name"] = data.get("doc_name")
        elif not data.get("nearBy"):
            filter["clinic_details.city"] = data.get("city")
        else:
            latitude = data.get("coordinates").get("latitude")
            longitude = data.get("coordinates").get("longitude")
            # latitude = 28.594983
            # longitude = 77.019331
            print(latitude, longitude)
            w = 0.01
            filter["clinic_details.latitude"] = {"$gte" : latitude-w, "$lte" : latitude+w }
            filter["clinic_details.longitude"] = {"$gte" : longitude-w, "$lte" : longitude+w }

        if data.get("spec"):
            filter["main_specialization"] = data.get("spec")
        if data.get("available"):
            filter["active"] = True
        # filter = {"_id" : "c4ca06e2486e"}
        print(filter)
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
        doctor = list(doctorsDb.find({"_id": doc_id}))
        if doctor:
            appmt = consultDb.update_one({"_id": appmt_id}, {"$set": {"doctor": doctor[0]}})
            return JsonResponse({"status": 1}, safe=False)
        else:
            return JsonResponse({"status" : -1, "msg" : "Doctor not found"})

from datetime import datetime

@login_required
def getDashboard(request, doc_id):
    ratings = list(ratingsDb.find({"doc_id": doc_id}))
    consult = list(consultDb.find({"doctor.user": doc_id, "completed": False}))
    "05/24/2022, 05:38:18"
    res = []
    for i in consult:
        timediff = ((datetime.now()-datetime.strptime(i["created_at"], "%d/%m/%Y, %H:%M:%S")).total_seconds())
        if timediff < 30*60:
            i["current"] = True
            res.append(i)
        else:
            consultDb.update_one({"_id" : i["_id"]}, {"$set":{ "completed" : True }})

    return JsonResponse(
        {"status": 1, "ratings": ratings, "consult": res}, safe=False
    )

def checkDoc(doc_id):
    res = doctorsDb.find({"_id": doc_id})
    if res:
        return res[0]

@login_required
@csrf_exempt
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
                doctorsDb.update_one({"_id" : doc_id}, {"$set" : {"online" : online, "active" : active}})
                return JsonResponse({"status" : 1}, safe=False)
            else:
                return JsonResponse({"status" : 403, "msg" : "Not Authorized"}, safe=False)
        else:
            return JsonResponse({"status" : 404, "msg" : "Doctor not found"}, safe=False)


@csrf_exempt
def getReviews(request, doc_id):
    print(doc_id)
    res = list(ratingsDb.find({"doc_id" : doc_id}))
    return JsonResponse({"status" : 1, "data" : res}, safe=False)

import re

@csrf_exempt
def getDoctorsByName(request):
    query = request.GET.get("query","").title()
    search_expr = re.compile(f"^{query}")
    print(query)
    # print(list(doctorsDb.distinct("name")))
    res = []
    if query:
        res = list(doctorNamesDb.find({"name" : search_expr}))
    # print(res)
    return JsonResponse({"status" : 1, "data": res}, safe=False)