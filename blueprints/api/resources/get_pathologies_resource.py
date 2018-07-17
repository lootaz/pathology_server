from flask_restful import Resource
from flask import request, current_app
import json

from common.models import PathologySelection, PathologyType, PathologyImage


class GetPathologiesByImageResource(Resource):
    def get(self, image_id = None):
        if not image_id:
            return "Pathology not found", 404

        pathologies = PathologySelection.query.filter(PathologySelection.pathology_image_id == image_id).all()

        response = {
            "amount": len(pathologies)
        }

        pathologies_response = []
        for pathology in pathologies:
            pathologies_response.append({
                "id": pathology.id,
                "dateCreated": str(pathology.create_ts),
                "p1": (pathology.p1x, pathology.p1y),
                "p2": (pathology.p2x, pathology.p2y),
                "type": pathology.pathology_type.name,
                'image_id': pathology.pathology_image.id,
            })
        response["pathologies"] = pathologies_response
        return response, 200

class GetPathologiesResource(Resource):

    def post(self):
        args_str = request.get_json()
        args = json.loads(args_str)

        amount = min(args.get("amount", 1), current_app.config.get("MAX_PATHOLOGY_PER_REQUEST", 1))
        start_date = args.get("startDate")

        query = PathologySelection.query
        pathology_selections_total = query.count()
        if start_date:
            query = query.filter(PathologySelection.create_ts > start_date)
        query = query.order_by(PathologySelection.create_ts)
        pathology_selections_filtered_amount = query.count()
        pathology_selections = query.limit(amount).all()


        response = {
            "total": pathology_selections_total,
            "amount": len(pathology_selections),
            "remainder": pathology_selections_filtered_amount - len(pathology_selections)
        }
        selections = []
        for selection in pathology_selections:
            type = selection.pathology_type
            image = selection.pathology_image
            selections.append({
                "dateCreated": str(selection.create_ts),
                "p1": (selection.p1x, selection.p1y),
                "p2": (selection.p2x, selection.p2y),
                "type": type.name,
                'image_id': image.id,
            })
        response["selections"] = selections

        return response, 200

class GetPathologyResource(Resource):
    def get(self, id = None):
        if not id:
            return "Pathology not found", 404

        pathology = PathologySelection.query.get(id)
        if not pathology:
            return "Pathology not found", 404

        response = {
            "id": pathology.id,
            "dateCreated": str(pathology.create_ts),
            "p1": (pathology.p1x, pathology.p1y),
            "p2": (pathology.p2x, pathology.p2y),
            "type": pathology.pathology_type.name,
            'image_id': pathology.pathology_image.id,
        }
        return response, 200





