from api.models import Doctor
import json
print("Running")
with open('UpdatingDoctors.json', encoding='utf-8') as f:
    j = json.loads(f.read())
    for i in range(100):
        a = j[i]
        d= Doctor.objects.create(name=a["name"], description=a.get("description", "N/A"))
        d.save()
        print(f"Created {d} ")

