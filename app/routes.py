from flask import Blueprint, jsonify, abort, request,make_response
from app.models.task import Task
from app import db
from app.helpers import validate_model, sort_title_asc, sort_title_desc
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    tasks = Task.query.all()
    response_body = []
    for task in tasks:
        response_body.append(task.to_dict())

    sort_query = request.args.get("sort")
    
    if sort_query and sort_query == "asc":
        return jsonify(sort_title_asc(response_body))
    elif sort_query and sort_query == "desc":
        return jsonify(sort_title_desc(response_body))
    else:
        return jsonify(response_body)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return make_response({"task":task.to_dict()}, 200)


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()
        return make_response({"task": new_task.to_dict()}, 201)
    
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))


@tasks_bp.route("/<task_id>", methods=["PUT"])
def replace_task(task_id):
    request_body = request.get_json()
    task_to_replace = validate_model(Task, task_id)
    try:
        task_to_replace.title = request_body["title"]
        task_to_replace.description = request_body["description"]
        if "competed_at" in request_body:
            task_to_replace.completed_at = request_body["completed_at"]

        db.session.commit()
        return make_response({"task": task_to_replace.to_dict()}, 200)
    
    except KeyError as error:
        abort(make_response({"details": "Invalid data"}, 404))



@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    message = f'Task {task_id} \"{task.title}\" successfully deleted'
    return make_response({"details": message}, 200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_complete(task_id):
    task_to_update = validate_model(Task, task_id)

    current_time = datetime.utcnow()
    
    task_to_update.completed_at = current_time

    db.session.commit()
    message = task_to_update.to_dict()
    return make_response({"task":message}, 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_incomplete(task_id):
    task_to_update = validate_model(Task, task_id)
    
    task_to_update.completed_at = None

    db.session.commit()
    message = task_to_update.to_dict()
    return make_response({"task":message}, 200)




    


    






    



