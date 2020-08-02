from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import desc


def configure_routes(app):
    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ornithologist:ornithologist@localhost:5432/birds_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Init db
    db = SQLAlchemy(app)
    # Init ma
    ma = Marshmallow(app)

    # Birds Class/Model
    class Birds(db.Model):
        species = db.Column(db.String(100))
        name = db.Column(db.String(100), primary_key=True)
        color = db.Column(db.String(100))
        body_length = db.Column(db.Integer)
        wingspan = db.Column(db.Integer)

        def __init__(self, species, name, color, body_length, wingspan):
            self.species = species
            self.name = name
            self.color = color
            self.body_length = body_length
            self.wingspan = wingspan

    # Birds Schema
    class BirdsSchema(ma.Schema):
        class Meta:
            fields = ('species', 'name', 'color', 'body_length', 'wingspan')

    # Init schema
    bird_schema = BirdsSchema()
    birds_schema = BirdsSchema(many=True)

    @app.route('/version', methods=['GET'])
    def get_version():
        return 'Birds Service. Version 0.1'


    # Get list of birds
    @app.route('/birds', methods=['GET'])
    def get_birds():
        if request.args.get('order') == 'desc' and request.args.get('attribute') in ['species', 'name', 'color',
                                                                                     'body_length', 'wingspan']:
            all_birds = Birds.query.order_by(desc(request.args.get('attribute'))) \
                .offset(request.args.get('offset') if 'offset' in request.args else 0) \
                .limit(request.args.get('limit') if 'limit' in request.args else None)

        elif request.args.get('order') == 'asc' and request.args.get('attribute') in ['species', 'name', 'color',
                                                                                      'body_length', 'wingspan']:
            all_birds = Birds.query.order_by(request.args.get('attribute')) \
                .offset(request.args.get('offset') if 'offset' in request.args else 0) \
                .limit(request.args.get('limit') if 'limit' in request.args else None)
        else:
            all_birds = Birds.query.offset(request.args.get('offset') if 'offset' in request.args else 0) \
                .limit(request.args.get('limit') if 'limit' in request.args else None)
        result = birds_schema.dump(all_birds)
        return jsonify(result)


    # Add new bird
    @app.route('/birds', methods=['POST'])
    def add_bird():
        species = request.json['species']
        name = request.json['name']
        color = request.json['color']
        body_length = request.json['body_length']
        wingspan = request.json['wingspan']
        new_bird = Birds(species, name, color, body_length, wingspan)
        db.session.add(new_bird)
        db.session.commit()
        return bird_schema.jsonify(new_bird)