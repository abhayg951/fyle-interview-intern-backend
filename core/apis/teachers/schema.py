from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from core.models.assignments import Teacher

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE

    created_at = auto_field(dump_only=True)
    id = auto_field(allow_none=True)
    updated_at = auto_field(dump_only=True)
    user_id = auto_field(dump_only=True)