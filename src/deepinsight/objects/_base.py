from pydantic import BaseModel


class BaseObject(BaseModel):
    @classmethod
    def from_db_model(cls, model: BaseModel):
        return cls.model_validate(model, from_attributes=True)

    def dump_dict(self):
        return self.model_dump(mode="json")
