<h1>FP Big Data - Movie ID Recommendations REST-API For Flixster User ID using Kafka and Flask</h1>
<p>By : Hanif Nashrullah (05111540000140)
<br>Dataset used: Flixster Data Set</p>

<h2>System</h2>
<ul>
  <li><h3>producer.py</h3></li>
  <p>Program that load and sent dataset to kafka server</p>
  <li><h3>consumer.py</h3></li>
  <p>Program that get dataset from kafka server and split it into batches. For configurations, i split dataset into 250000 lines for each batch</p>
  <li><h3>app.py</h3></li>
  <p>Program that routes retrieved request and call function to create recommendation based on request</p>
  <li><h3>engine.py</h3></li>
  <p>Core of data processing, load dataset batches and create recommendations model(s). This program creates n models and each model load different amount of lines based on amount of models (Example : Amount of models = 4, Model 1 loads 1/4 of datasets, Model 2 loads 2/4 of datasets, ... , Model 4 loads 4/4 of datasets). For configurations, this program creates 3 models.</p>
  <li><h3>server.py</h3></li>
  <p>Main program to initialize other programs, runs on CherryPyr</p>
</ul>

<h2>How To Use</h2>
<ol>
  <li>Run Zookeeper. Tutorial for Zookeeper can be accessed at https://medium.com/@shaaslam/installing-apache-zookeeper-on-windows-45eda303e835</li>
  <li>Run Kafka. Tutorial for Zookeeper can be accessed at https://medium.com/@shaaslam/installing-apache-kafka-on-windows-495f6f2fd3c8</li>
  <li><p>Create a new topic. For configuration, i create 'ratings' topic. Run this code on kafka directory.</p><code>.\bin\windows\kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic ratings</code></li>
  <li>Run producer.py</li>
  <li>Run consumer.py</li>
  <li>Run server.py</li>
  <li>Open http://localhost:6136/recommendations/ from browser</li>
  <li>Fill User ID, amount of recommendations, and model used</li>
  <li>Click 'Get Recommendations'</li>
</ol>

<h2>Implementation</h2>
