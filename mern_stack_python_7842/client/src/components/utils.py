from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Blog API', description='A simple blog API')

# Define a namespace for styles
styles_ns = api.namespace('styles', description='Styles operations')

# Define a model for the styles
style_model = api.model('Style', {
    'font': fields.String(required=True, description='Font family')
})

@styles_ns.route('/')
class Styles(Resource):
    @styles_ns.doc('get_styles')
    @styles_ns.marshal_with(style_model)
    def get(self):
        """Get the styles"""
        return {'font': 'Roboto !important'}

if __name__ == '__main__':
    app.run(debug=True)