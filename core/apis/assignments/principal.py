from flask import Blueprint
from core import db
from core.apis import decorators, responses
from core.models.assignments import Assignment, AssignmentStateEnum
from .schema import AssignmentSchema, AssignmentGradeSchema
from ..teachers.schema import TeacherSchema
from core.models.teachers import Teacher

principal_assignments_resources = Blueprint('principle_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'])
@decorators.authenticate_principal
def list_assignments(p):
    """Return List all submitted and graded assignments"""
    principle_assignments = Assignment.get_assignments_by_principal(p.principal_id)
    principal_assignments_dump = AssignmentSchema().dump(principle_assignments, many=True)
    return responses.APIResponse.respond(data=principal_assignments_dump)

@principal_assignments_resources.route('/teachers', methods=['GET'])
@decorators.authenticate_principal
def list_teachers(p):
    """Return List all the teachers"""
    db_query = db.session.query(Teacher).all()
    teachers_dump = TeacherSchema().dump(db_query, many=True)
    return responses.APIResponse.respond(data=teachers_dump)

@principal_assignments_resources.route("/assignments/grade", methods=["POST"])
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignments(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    # fetching the assignment
    assignment = Assignment.query.filter(Assignment.id == grade_assignment_payload.id).all()
    assignment_values = AssignmentSchema().dump(assignment, many=True)
    assignment_state = assignment_values[0]['state']
    if assignment_state == AssignmentStateEnum.DRAFT:
        response = responses.APIResponse.respond(data="Assignment cannot be graded")
        response.status_code = 400
        return response
    
    
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment) 
    return responses.APIResponse.respond(data=graded_assignment_dump)