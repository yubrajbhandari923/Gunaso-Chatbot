from api.models import Hospital
import json
print("Running")
with open('Hospitals.json', encoding='utf-8') as f:
    j = json.loads(f.read())
    for i in range(100):
        a = j[i]
        try:
            d= Hospital.objects.create(name=a["name"], address=a.get('address', "N/A"))
            d.save()
        except Exception:
            continue
        print(f"Created {d} ")

