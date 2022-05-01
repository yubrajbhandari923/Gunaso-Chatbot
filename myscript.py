from api.models import Doctor
import json

with open('UpdatingDoctors.json') as f:
    j = json.loads(f.read())
    print(j)
    # for i in range(100):

