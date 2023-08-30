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

    class Config:
        schema_extra = {"example": {
            "id": 112946,
            "title": "Как программировать на HDMI",
            "organizer": "Senior HDMI Developer",
            "audience": "Хлебушек",
            "organizer": "Представитель образовательной организации",
            "seatsPropotion": "100/200",
            "date": "09.07.2023, 17:00:00",
            "startTime": "2023-07-09T17:00:00.000Z",
            "finishTime": "2023-07-09T20:00:00.000Z"
        }}


class OlimpiadsParsed(BaseModel):
    id: int