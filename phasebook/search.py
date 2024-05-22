from flask import Blueprint, request, jsonify

from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    return jsonify(search_users(request.args.to_dict())), 200

def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    filtered_users = USERS
    results = []

    if "id" in args:
        results.extend([user for user in filtered_users if user["id"] == args["id"]])

    if "name" in args:
        results.extend([user for user in filtered_users if args["name"].lower() in user["name"].lower()])

    if "age" in args:
        results.extend([user for user in filtered_users if str(user["age"]) == args["age"]])

    if "occupation" in args:
        results.extend([user for user in filtered_users if args["occupation"].lower() in user["occupation"].lower()])

    results = [dict(t) for t in {tuple(d.items()) for d in results}]

    def sort_key(user):
        priority = 0
        if "id" in args and user["id"] == args["id"]:
            priority += 1
        if "name" in args and args["name"].lower() in user["name"].lower():
            priority += 2
        if "age" in args and str(user["age"]) == args["age"]:
            priority += 3
        if "occupation" in args and args["occupation"].lower() in user["occupation"].lower():
            priority += 4
        return -priority 

    results.sort(key=sort_key, reverse=True)

    return results
