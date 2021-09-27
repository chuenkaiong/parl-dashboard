import requests
import streamlit as st
import numpy as np
import json
import pandas as pd
from bs4 import BeautifulSoup

st.title("STREAMLIT TESTING")

dates = ['24-08-2020', '31-08-2020', '01-09-2020', '02-09-2020', '03-09-2020', '04-09-2020', '05-10-2020', '06-10-2020', '14-10-2020', '15-10-2020', '02-11-2020', '03-11-2020', '04-11-2020', '04-01-2021', '05-01-2021', '01-02-2021', '02-02-2021', '16-02-2021', '24-02-2021', '25-02-2021', '26-02-2021', '01-03-2021', '02-03-2021', '03-03-2021', '04-03-2021', '05-03-2021', '08-03-2021', '05-04-2021', '10-05-2021', '11-05-2021']

attendanceCounts = {}

# with open("sitting_data/24-08-2020.json","r") as f:
#   output = json.load(f)

@st.cache
def get_mp_info():
  r = requests.get('https://www.parliament.gov.sg/mps/list-of-current-mps')
  soup = BeautifulSoup(r.text)

  mps = []
  for div in soup('div', class_='row list-of-mps-wrap'):
    a = div.find('a')
    r = requests.get('https://www.parliament.gov.sg' + a.get('href'))
    details_soup = BeautifulSoup(r.text, features="html.parser")
    party_div = details_soup.find('div', class_='row mp-party-wrap')
    party = party_div('div')[-1].get_text(strip=True)
    if party.isnumeric():
      party = "NA"
    name = a.get_text(strip=True)
    const_div = div.find('div', class_='col-md-6 col-xs-11 mp-sort constituency')
    constituency = const_div.get_text(strip=True)
    mps.append((name, constituency, party))
    
  return mps

"This app displays information about Parliamentary sittings from a small test sample dataset, from 13 Aug 2020 to 1 Feb 2021. More will be added in the future."

st.markdown("## MP Attendance Metrics")
if st.checkbox("View MP attendance metrics (requires a one-time load)"):
  mps = get_mp_info()

  # TODO: cache this? 
  for date in dates:
    with open(f"sitting_data/{date}.json","r", encoding="utf-8") as f:
      data = json.load(f)

      attendanceList = data["attendanceList"]
      for mp in attendanceList:
        name = mp["mpName"]
        if name not in attendanceCounts:
          attendanceCounts[name] =  [0, "NA"]
        if mp["attendance"] == True:
          attendanceCounts[name][0] += 1

  # add MP's party affiliation to attendance count

  for mpTitle in attendanceCounts:
    for mp_details in mps:
      if mp_details[0] in mpTitle:
        party = mp_details[2]
        attendanceCounts[mpTitle][1] = party
        break
    
  attendance = pd.DataFrame.from_dict(attendanceCounts, orient="index", columns=[f"Sessions attended", "Party"])
  attendance


st.markdown("## MP participation scores by sitting and topic")
participation_date = st.selectbox("Select sitting date to view", options=dates)

with open(f"sitting_data/{participation_date}.json","r", encoding="utf-8") as f:
    data = json.load(f)
    
    participation_options = [(i, section["title"]) for i,section in enumerate(data["takesSectionVOList"])]

    participation_topic = st.selectbox("Select a topic", options=participation_options)
    
    
    participation_blob = data["takesSectionVOList"]
    soup = BeautifulSoup(data["takesSectionVOList"][participation_topic[0]]["content"], features="html.parser")

    speakerCounts = {}

    speakerNames = soup.find_all("strong")
    for speaker in speakerNames:
        speaker = speaker.string.strip()
        if speaker != "" and "Speaker" not in speaker:
            if speaker not in speakerCounts:
                speakerCounts[speaker] = 1
            else:
                speakerCounts[speaker] += 1
    
    st.write(pd.DataFrame.from_dict(speakerCounts, orient="index", columns=["Number of times spoken"]))
