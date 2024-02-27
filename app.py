from flask import Flask,render_template,request,url_for,redirect
import asyncio
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os
connstr = os.environ['connection_string']
queue_name = "customerqueue"

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def details_form():
    return render_template('details.html')
@app.route('/Queuepush',methods=['GET','POST'])
def push_msg():
    if request.method=='POST':
        name=str(request.form['firstName'])
        lastname=str(request.form['lastName'])
        age=str(request.form['age'])
        gender=str(request.form['gender'])
        occupation=str(request.form['occupation'])
        country=str(request.form['country'])
        dict={
        "FirstName":name,
        "LastName":lastname,
        "Age":age,
        "Gender":gender,
        "Occupation":occupation,
        "Country":country
         }
        with ServiceBusClient.from_connection_string(connstr) as client:
            with client.get_queue_sender(queue_name) as sender:
                single_message = ServiceBusMessage(str(dict))
                try:
                    sender.send_messages(single_message)
                    print("Message pushed to Queue successfully"+ str(dict))
                except:
                    print("Message not pushed into the queue.")

        return "Signup Successful"
    return "Form not submitted"

if __name__=='__main__':
    app.run(debug=True,port=8080)