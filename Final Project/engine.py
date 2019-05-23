from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
import pandas as pd
from pyspark.sql import functions
import os

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEngine:
    """A Flixster movie recommendation engine
    """

    def __init__(self, spark, ds_batch_folder):
        """Init the recommendation engine given a Spark context and a dataset batch path
        """

        # Load dataset
        n_batch = 0
        while True:
            ds_batch_path = os.path.join(ds_batch_folder, ('ratings-batch-' + str(n_batch) + '.txt'))
            exist = os.path.isfile(ds_batch_path)
            if exist:
                logger.info("Loading dataset batch %s...", n_batch)
                lines = spark.read.text(ds_batch_path).rdd
                parts = lines.map(lambda row: row.value.split("\t"))
                datasetRDD = parts.map(lambda p: Row(userid=int(p[0]), movieid=int(p[1]), rating=float(p[2])))
                if n_batch > 0 :
                    newdataframe = spark.createDataFrame(datasetRDD)
                    self.dataframe = self.dataframe.union(newdataframe)
                else:
                    self.dataframe = spark.createDataFrame(datasetRDD)
                n_batch += 1
            else:
                break
        self.dataframe.dropDuplicates()
        n_lines = self.dataframe.count()
        logger.info("Dataset loaded (%s lines).", n_lines)

        # Start train
        self.__train_model()

    def __train_model(self):
        """Train the ALS model with the current dataset
        """
        logger.info("Training the ALS model(s)...")

        model_amount = 3
        self.model = []
        n_lines = self.dataframe.count()
        for n_model in range(model_amount):
            n_lines_model = int(n_lines / model_amount * (n_model + 1))
            train = self.dataframe.limit(n_lines_model)

            logger.info("Training model %s (%s lines)...", n_model, n_lines_model)

            # Build the recommendation model using ALS on the training data
            # Note we set cold start strategy to 'drop' to ensure we don't get NaN evaluation metrics
            als = ALS(maxIter=5, regParam=0.01, userCol="userid", itemCol="movieid", ratingCol="rating", coldStartStrategy="drop")
            temp_model = als.fit(train)
            self.model.append(temp_model)

        logger.info("Done build model(s).")



    def get_recommendations(self, userid, n_model, n):
        if n_model >= len(self.model):
            return str("Model is not exist.")
        Recs = self.model[n_model].recommendForAllUsers(n)
        userRecs = Recs.where(Recs.userid == userid).limit(1)
        if userRecs is None:
            return [0, str("User is not exist.")]
        if (userRecs.count() == 0):
            return [0, str("Not Enough data for recommendation.")]
        # userRecs = userRecs.toPandas()
        # userRecs = userRecs.to_json()

        def mapping(line):
            return [x for x in line]

        r = userRecs.select("recommendations").collect()[0][0]
        li = list(map(mapping, r))
        return [1, li]
        # return userRecs
