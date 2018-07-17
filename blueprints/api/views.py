from flask import Blueprint
from flask_restful import Api
from .resources.pathology_image_resource import PathologyImageResource
from .resources.get_pathologies_resource import GetPathologiesResource, GetPathologyResource, GetPathologiesByImageResource
from .resources.get_pathology_images_resource import GetPathologiesImagesResource, GetPathologyImageResource

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

api.add_resource(PathologyImageResource, "/pathology")
api.add_resource(GetPathologiesResource, "/get_pathologies")
api.add_resource(GetPathologyResource, "/get_pathology/<id>")
api.add_resource(GetPathologiesByImageResource, "/get_pathologies_by_image/<image_id>")
api.add_resource(GetPathologiesImagesResource, "/get_pathology_images")
api.add_resource(GetPathologyImageResource, "/get_pathology_image/<id>")


