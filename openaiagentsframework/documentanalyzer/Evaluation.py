from pydantic import BaseModel
class Evaluation(BaseModel):
    isAcceptable: bool
    feedback: bool