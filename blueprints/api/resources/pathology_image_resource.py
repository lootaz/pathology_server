import os
import datetime
import json
from flask_restful import Resource
from flask import request, current_app, redirect, url_for
from werkzeug.utils import secure_filename

from common.models import PathologyImage, PathologySelection, PathologyType, db


class PathologyImageResource(Resource):
    def allowed_file(self, filename):
        return True

    def get(self):
        return "Hello", 200

    def post(self):
        filename = self.save_file()
        if not filename:
            return "File not found", 400
        p_image = PathologyImage(filename)

        pathologies_value = request.values['pathologies']
        if not pathologies_value:
            return "Pathology data not found", 400
        pathologies = json.loads(pathologies_value)
        for pathology in pathologies:
            p_selection = PathologySelection(pathology["p1x"],
                                             pathology["p1y"],
                                             pathology["p2x"],
                                             pathology["p2y"])
            p_type = PathologyType.query.filter_by(name=pathology['type']).first()
            if not p_type:
                p_type = PathologyType(pathology['type'])

            p_selection.pathology_type = p_type
            p_selection.pathology_image = p_image
            db.session.add(p_selection)

        db.session.commit()

        return "OK", 200

    def save_file(self):
        if 'file' not in request.files:
            return None

        file = request.files['file']
        if file.filename == '':
            return None

        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_folder = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.%f")
        upload_path = os.path.join(upload_folder, file_folder)
        os.makedirs(upload_path)
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_path, filename)
        file.save(filepath)

        return filepath
