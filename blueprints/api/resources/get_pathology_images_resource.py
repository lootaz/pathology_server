from flask_restful import Resource
from flask import request, current_app, send_file
import json
import os

from common.models import PathologySelection, PathologyType, PathologyImage


class GetPathologiesImagesResource(Resource):
    def post(self):
        args_str = request.get_json()
        args = json.loads(args_str)

        amount = min(current_app.config.get("MAX_PATHOLOGY_PER_REQUEST", 1), args.get('amount', 1))
        start_date = args.get("startDate")

        query = PathologyImage.query
        pathology_image_total = query.count()
        if start_date:
            query = query.filter(PathologyImage.create_ts > start_date)
        query = query.order_by(PathologyImage.create_ts)
        pathology_image_filtered_amount = query.count()
        pathology_images = query.limit(amount).all()

        response = {
            "total": pathology_image_total,
            "amount": len(pathology_images),
            "remainder": pathology_image_filtered_amount - len(pathology_images)
        }

        images = []
        for image in pathology_images:
            images.append({
                "id": image.id,
                "dateCreated": str(image.create_ts),
                "filename": os.path.basename(image.path)
            })
        response['images'] = images

        return response, 200

class GetPathologyImageResource(Resource):
    def get(self, id = None):
        if not id:
            return "Image not found", 404

        image = PathologyImage.query.get(id)
        if not image:
            return "Image not found", 404
        return send_file(image.path, mimetype="image/png")