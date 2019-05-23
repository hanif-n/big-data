<h1>FP Big Data - Movie ID Recommendations RESTT-API For Flixster User ID using Kafka and Flask</h1>
<p>By : Hanif Nashrullah (05111540000140)
Dataset used: Flixster Data Set</p>

<h2>System</h2>
<ul>
  <li><h4>producer.py</h4></li>
  <p>Program that load and sent dataset to kafka server</p>
  <li><h4>consumer.py</h4></li>
  <p>Program that get dataset from kafka server and split it into batches. For configurations, i split dataset into 250000 lines for each batch</p>
  <li><h4>app.py</h4></li>
  <p>Program that routes retrieved request and call function to create recommendation based on request</p>
  <li><h4>engine.py</h4></li>
  <p>Core of data processing, load dataset batches and create recommendations model(s). This program creates n models and each model load different amount of lines based on amount of models (Example : Amount of models = 4, Model 1 loads 1/4 of datasets, Model 2 loads 2/4 of datasets, ... , Model 4 loads 4/4 of datasets). For configurations, this program creates 3 models.</p>
  <li><h4>server.py</h4></li>
  <p>Main program to initialize other programs, runs on CherryPyr</p>
</ul>

