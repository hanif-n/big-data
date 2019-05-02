import time, sys, cherrypy, os
import logging
from paste.translogger import TransLogger
from app import create_app
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import findspark

findspark.init()

# Create Spark Session
print("Initialize Spark session...")
spark = SparkSession.builder.appName("Reddit Submissions Recommendation Engine").getOrCreate()

def run_server(app):
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')

    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 6136,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    print("Starting engine...")
    cherrypy.engine.start()
    print("Engine has been started.")
    cherrypy.engine.block()


if __name__ == "__main__":
    # IMPORTANT: pass aditional Python modules to each worker
    enginepyloc = os.path.join(os.getcwd(), "engine.py")
    apppyloc = os.path.join(os.getcwd(), "app.py")
    spark.sparkContext.addPyFile(enginepyloc)
    spark.sparkContext.addPyFile(apppyloc)

    #set dataset location
    dataset_path = os.path.join(os.getcwd(), 'submissions.csv')
    app = create_app(spark, dataset_path)

    # start web server
    run_server(app)