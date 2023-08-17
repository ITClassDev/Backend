from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from app import settings
from typing import List
import requests
from app.events.schemas import EventsMosParsed

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
    



@router.get("/generic", response_model=List[EventsMosParsed])
async def parse_school_events():
    pass