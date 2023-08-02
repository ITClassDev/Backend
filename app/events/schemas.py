from pydantic import BaseModel

class EventsMosParsed(BaseModel):
    id: int
    title: str
    organizer: str
    audience: str
    seatsPropotion: str
    date: str
    startTime: str
    finishTime: str