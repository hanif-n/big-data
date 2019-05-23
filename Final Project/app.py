from flask import Flask, Blueprint, render_template, request
main = Blueprint('main', __name__)

import json
from engine import RecommendationEngine

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Flask, request

@main.route("/recommendations", methods=["GET", "POST"])
def get_recommendations():
    if request.method == 'GET':
        return render_template('recommendationsForm.html')
    elif request.method == 'POST':
        userid = int(request.form.get('userid'))
        n_model = int(request.form.get('n_model'))
        n = int(request.form.get('n'))
        logger.debug("Get %s recommendation(s) for user %s using model %s", n, userid, n_model)
        recommendations = recommendation_engine.get_recommendations(userid, n_model, n)
        if recommendations[0]:
            return render_template('recommendationsGet.html', recommendations=recommendations[1], userid=userid)
        else:
            return render_template('recommendationsError.html', recommendations=recommendations[1])


def create_app(spark_context, dataset_path):
    global recommendation_engine

    recommendation_engine = RecommendationEngine(spark_context, dataset_path)

    app = Flask(__name__)
    app.register_blueprint(main)
    return app
