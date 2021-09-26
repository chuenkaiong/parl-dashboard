import json
from bs4 import BeautifulSoup

with open("sitting_data/01-02-2021.json","r", encoding="utf-8") as f:
    data = json.load(f)

    print("Topics: ", list(map(lambda section: section["title"], data["takesSectionVOList"])))
    print("\n" * 2)
    soup = BeautifulSoup(data["takesSectionVOList"][4]["content"], features="html.parser")

    speakerCounts = {}

    speakerNames = soup.find_all("strong")
    for speaker in speakerNames:
        speaker = speaker.string.strip()
        if speaker != "":
            if speaker not in speakerCounts:
                speakerCounts[speaker] = 1
            else:
                speakerCounts[speaker] += 1
    
    print(speakerCounts)
    