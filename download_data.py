import json
import requests

dates = ['24-08-2020', '31-08-2020', '01-09-2020', '02-09-2020', '03-09-2020', '04-09-2020', '05-10-2020', '06-10-2020', '14-10-2020', '15-10-2020', '02-11-2020', '03-11-2020', '04-11-2020', '04-01-2021', '05-01-2021', '01-02-2021', '02-02-2021', '16-02-2021', '24-02-2021', '25-02-2021', '26-02-2021', '01-03-2021', '02-03-2021', '03-03-2021', '04-03-2021', '05-03-2021', '08-03-2021', '05-04-2021', '10-05-2021', '11-05-2021']
# dates = ['24-08-2020', '31-08-2020']

url = 'https://sprs.parl.gov.sg/search/getHansardReport/?sittingDate='

r = requests.post(url + dates[0])

for date in dates: 
  r = requests.post(url + date)
  with open(f"sitting_data/{date}.json", "w", encoding="utf-8") as f:
    json.dump(r.json(), f, ensure_ascii=False, indent=4)