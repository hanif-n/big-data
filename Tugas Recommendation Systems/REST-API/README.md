<h1>Reddit Submissions REST-API</h1>
REST-API for recommendations of thread in Reddit Submissions. This application retrieve request and send recommendations.
There are several programs that runs on this application :
<ul>
<li>app.py : routes retrieved request and call function to create recommendation based on request</li>
<li>engine.py : core of data processing, create recommendations model</li>
<li>server.py : main program to initialize other programs, runs on CherryPy</li>
</ul>

<h2>How to use</h2>
Place dataset, app.py, engine.py, and server.py in one directory. Dataset could be downloaded at https://snap.stanford.edu/data/web-Reddit.html.
Then run "python server.py" on cmd/terminal.

Recommendations cold be requested via HTTP GET method :

<h3>http://[IP_SERVER]:6136/user-recs-for-thread/[INT]/</h3>
Request [INT] user recommendations for each thread/reddit_id.<br>
Example :
<img src=""/>

<h3>http://[IP_SERVER]:6136/thread-recs-for-user/[INT]/</h3>
Request [INT] thread/reddit_id recommendations for each user.<br>
Example :
<img src=""/>
