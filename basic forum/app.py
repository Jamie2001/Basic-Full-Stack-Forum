from flask import Flask, session, request, url_for, render_template, jsonify
import mysql.connector, json

app = Flask(__name__)
app.secret_key = b'798ed0d2aaa182ee4bf1225173a474d52f13ed897526015ae30f933acded1f95'
mydb= mysql.connector.connect(
    host="localhost",
    user="root",
    password="1922",
    database="forumdata"
)
cursor = mydb.cursor()
#cursor.execute("SELECT * FROM topic")
#myresult = mycursor.fetchall()

Topic=[]
# for TopicID, Header, Contents in cursor:
#     topicData={"TopicID":TopicID,"Header":Header,"Contents":Contents}
#     Topic.append(topicData)


@app.route('/')
def index():
     return render_template("home.html")
     

@app.route('/home', methods = ['GET'])
def home():
    cursor.execute("SELECT * FROM topic")
    Topic=[]
    for TopicID, Header, Contents in cursor:
        topicData={"TopicID":TopicID,"Header":Header,"Contents":Contents}
        Topic.append(topicData)

    return (json.dumps(Topic))


@app.route('/Topic/<TopicID>')
def topic(TopicID):
    session["TopicID"]=TopicID
    return render_template('topic.html')
     

@app.route('/fetchClaims', methods = ['GET'])
def Claim(): 
    Topic=session["TopicID"]
    fetch = "select header, content, posterID, ClaimID FROM claim where parentTopicID = %s"
    cursor.execute(fetch, (Topic, ))
    Claim=[]
    for header, content, posterID, ClaimID in cursor:
        claimData={"header":header,"content":content, "posterID":posterID, "ClaimID":ClaimID}
        Claim.append(claimData)
    return (json.dumps(Claim))
    
@app.route('/Claim/<ClaimID>')
def claim(ClaimID):
    session["ClaimID"]=ClaimID
    return render_template('Claim.html')

@app.route('/fetchReplys', methods = ['GET'])
def reply(): 
    Claim=session["ClaimID"]
    fetch = "select replyID, posterID, contents, argumentType FROM reply where parentClaimID = %s"
    cursor.execute(fetch, (Claim, ))
    Reply=[]
    for replyID, posterID, contents, argumentType in cursor:
        replyData={"replyID":replyID, "posterID":posterID, "contents":contents, "argumentType":argumentType}
        Reply.append(replyData)
    return (json.dumps(Reply))











