from api.models import Ambulance
import json
print("Running")
with open('Ambulnace.json', encoding='utf-8') as f:
    j = json.loads(f.read())
    for i in range(100):
        a = j[i]
        d= Ambulance.objects.create(name=a["name"], description=a.get("description", "N/A"), hospital_name=a.get("hospital_name", "N/A"), phone=int(a.get("phone", "0")), image=a.get("image", "N/A"))
        d.save()
        print(f"Created {d} ")

