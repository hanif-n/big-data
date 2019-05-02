from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
import pandas as pd
from pyspark.sql import functions

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEngine:
    """A item recommendation engine
    """

    def __init__(self, spark, dataset_path):
        """Init the recommendation engine given a Spark context and a dataset path
        """
        self.spark = spark

        # Load dataset
        logger.info("Loading dataset...")
        self.submissions = spark.read.csv(dataset_path, header=True, inferSchema=True)
        self.sub = self.submissions.select("username", "reddit_id", "score").filter("username is not null")

        # Get min score in dataframe
        self.sub_min = self.sub.agg({"score": "min"}).collect()[0]
        self.min_score = self.sub_min["min(score)"]

        # Get max score in dataframe
        self.sub_max = self.sub.agg({"score": "max"}).collect()[0]
        self.max_score = self.sub_max["max(score)"]

        # Normalize score into scale between 0 to 10
        self.score_normalized = self.sub.select("reddit_id", ((self.sub.score - self.min_score)/(self.max_score - self.min_score)*10).alias("score_normalized"))
        
        # Assign id for each distinct username
        self.username = self.sub.select("username").distinct()
        self.username_id_schema = self.username.withColumn("username_id", functions.lit(1)).schema
        self.rdd_username_id = self.username.rdd.zipWithIndex().map(lambda row_rowId: (list(row_rowId[0]) + [row_rowId[1] + 1]))
        self.username_id = spark.createDataFrame(self.rdd_username_id, self.username_id_schema)

        # Assign id for each distinct reddit_id
        self.reddit_id = self.sub.select("reddit_id").distinct()
        self.reddit_id_id_schema = self.reddit_id.withColumn("reddit_id_id", functions.lit(1)).schema
        self.rdd_reddit_id_id = self.reddit_id.rdd.zipWithIndex().map(lambda row_rowId: (list(row_rowId[0]) + [row_rowId[1] + 1]))
        self.reddit_id_id = spark.createDataFrame(self.rdd_reddit_id_id, self.reddit_id_id_schema)

        #Join id tables with data table
        self.sub = self.sub.join(self.username_id, "username")
        self.sub = self.sub.join(self.reddit_id_id, "reddit_id")
        self.sub = self.sub.join(self.score_normalized, "reddit_id")

        # Select processed columns from joined table
        self.s = self.sub.select('username_id', 'reddit_id_id', 'score_normalized')

        logger.info("Dataset loaded")

        # Start train
        self.__train_model()

    def __train_model(self):
        """Train the ALS model with the current dataset
        """
        logger.info("Training the ALS model...")

        # Train, Test
        (train, test) = self.s.randomSplit([0.8,0.2])

        # Build the recommendation model using ALS on the training data
        # Note we set cold start strategy to 'drop' to ensure we don't get NaN evaluation metrics

        als = ALS(maxIter=5, regParam=0.01, userCol="username_id", itemCol="reddit_id_id", ratingCol="score_normalized", coldStartStrategy="drop")

        self.model = als.fit(train)

        logger.info("Done build ALS.")

    def get_rec_user(self, numItems):

        userRecs = self.model.recommendForAllUsers(numItems)
        userRecs = userRecs.toPandas()
        userRecs = userRecs.to_json()

        return userRecs

    def get_rec_thread(self, numUsers):

        itemRecs = self.model.recommendForAllItems(numUsers)
        itemRecs = itemRecs.to_json()
        itemRecs = itemRecs.toPandas()
        
        return itemRecs
