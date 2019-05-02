from flask import Blueprint
main = Blueprint('main', __name__)
 
import json
from engine import RecommendationEngine
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, request
 
@main.route("/user-recs-for-thread/<int:count>/", methods=["GET"])
def get_rec_thread(count):
    logger.debug("Thread %s TOP user recommendations", count)
    top_user = recommendation_engine.get_rec_thread(count)
    return json.dumps(top_user)
 
 
@main.route("/thread-recs-for-user/<int:count>/", methods = ["GET"])
def get_rec_user(count):
    logger.debug("User %s TOP thread(s) recommendations", count)
    top_thread = recommendation_engine.get_rec_user(count)
    return json.dumps(top_thread)
 
 
def create_app(spark_context, dataset_path):
    global recommendation_engine 

    recommendation_engine = RecommendationEngine(spark_context, dataset_path)    
    
    app = Flask(__name__)
    app.register_blueprint(main)
    return app 