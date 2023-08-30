from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from app import settings
from typing import List
import requests
from app.events.schemas import EventsMosParsed, OlimpiadsParsed
from bs4 import BeautifulSoup

router = APIRouter()


@router.get("/profil", response_model=List[EventsMosParsed])
async def parse_events_from_profil_mos():
    # This module is very unstable and can works unexpected, because this is based on graphql of profil.mos.ru
    # Note, that we use sync http requests
    payload = {
        "operationName": None,
        "variables": {
            "onlyActual": True,
            "pageNumber": 1,
            "search": "",
            "startDate": "2022-12-30",
            "portalIds": [settings.profil_category],
            "districtIds": [],
            "agentIds": [],
            "formeIds": [],
            "audienceIds": [],
            "subjectIds": [],
            "participationTypes": [],
        },
        "query": "query ($portalIds: [Int!], $startDate: String, $finishDate: String, $agentIds: [Int!], $districtIds: [Int!], $formeIds: [Int!], $audienceIds: [Int!], $subjectIds: [Int!], $search: String, $pageNumber: Int, $onlyActual: Boolean, $orderDays: String, $archive: Boolean, $elasticsearch: Boolean, $participationTypes: [Int!]) {\n  eventsList(portalIds: $portalIds, startDate: $startDate, finishDate: $finishDate, agentIds: $agentIds, districtIds: $districtIds, formeIds: $formeIds, audienceIds: $audienceIds, subjectIds: $subjectIds, search: $search, pageNumber: $pageNumber, onlyActual: $onlyActual, orderDays: $orderDays, archive: $archive, elasticsearch: $elasticsearch, participationTypes: $participationTypes) {\n    pagesCount\n    maxArchiveStartDate\n    maxArchiveFinishDate\n    selectedStartDate\n    selectedFinishDate\n    events {\n      id\n      title\n      seats\n      reservedSeats\n      emptySeats\n      additionalSeats\n      emptySeatsOnline\n      reservedSeatsOnline\n      seatsOnline\n      date\n      startTime\n      finishedTime\n      startRegistration\n      finishedRegistration\n      markEvent\n      audiencesShort\n      participationTypes\n      comments {\n        id\n        reaction {\n          id\n          __typename\n        }\n        __typename\n      }\n      portal {\n        id\n        name\n        logoImage\n        host\n        markEventText\n        markEventImage\n        __typename\n      }\n      audiences {\n        id\n        name\n        __typename\n      }\n      formes {\n        id\n        name\n        __typename\n      }\n      subject {\n        id\n        name\n        __typename\n      }\n      agent {\n        id\n        name\n        logoImage\n        logo {\n          large\n          medium\n          __typename\n        }\n        __typename\n      }\n      house {\n        address\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
    }
    response = requests.post(settings.profil_endpoint, json=payload).json()["data"]["eventsList"]["events"]
    return [EventsMosParsed(id=event["id"], title=event["title"], 
                organizer=event["agent"]["name"], audience=event["audiencesShort"][0],
                seatsPropotion=f"{event['emptySeats'] + event['emptySeatsOnline']}/{event['seats'] if event['seats'] else 0 + event['seatsOnline']}", date=event["date"], startTime=event["startTime"], finishTime=event["finishedTime"]) for event in response]
    


@router.get("/olimpiads/{forClass}", response_model=List[OlimpiadsParsed])
async def parse_olimpiads_ru(forClass: int):
    '''
    curl 'https://olimpiada.ru/include/activity/megalist.php?class=10&type=any&period_date=&period=year' 
    --compressed -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0' 
    -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' 
    -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' 
    -H 'Referer: https://olimpiada.ru/activities?class=10&type=any&period_date=&period=year' 
    -H 'Cookie: __ddg1_=UIQ2DXs2889sdD4H9HvT; region=77; tmr_vid_5756=1; 
    ADD &cnow=20
    SUBJECT 7 - Informatics 
    '''
    print(forClass)
    count = requests.get(f"https://olimpiada.ru/include/activity/megatitle.php?subject[7]=on&class={forClass}&type=any&period_date=&period=year").text
    print(count)
    count = int(count.split()[0])
    html = requests.get(f"https://olimpiada.ru/include/activity/megalist.php?subject[7]=on&class={forClass}&type=any&period_date=&period=year").text
    soup = BeautifulSoup(html, 'html.parser')
    return []

@router.get("/school", response_model=List[EventsMosParsed])
async def get_school_events():
    pass