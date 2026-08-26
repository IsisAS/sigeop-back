from pydantic import BaseModel, ConfigDict


class ReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class CreateSchema(BaseModel):
    pass

class UpdateSchema(BaseModel):
    pass