from flask import Flask, render_template, request, session
import requests
import numpy as np
from sklearn.cluster import KMeans

app = Flask(__name__)
#app._static_folder = "/assets"

app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
@app.route('/')
def dashboard():
    
    heartRate = np.random.randint(35,105,(200,1));
    lowBpSys = np.random.randint(85,120,(200,1));
    lowBpDia = np.random.randint(55,80,(200,1));
    highBpDia = np.random.randint(85,95,(200,1));
    highBpSys = np.random.randint(120,145,(200,1));
    temp = np.random.randint(94,102,(200,1))
    spo = np.random.randint(92,99,(200,1))
    
    dataSet = np.append(lowBpSys,lowBpDia,1)
    data1 = np.append(dataSet,highBpDia,1)
    data2 = np.append(data1,highBpSys,1)
    data3 = np.append(data2,temp,1)
    data4 = np.append(data3,spo,1)
    data5 = np.append(data4,heartRate,1)
    #data6 = np.append(data5,np.transpose(range(1,201)))
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=10, random_state=0).fit(data5)
    #kmeans.labels_
    jsonData = {
      "array":kmeans.labels_.tolist() ,
      "object": {
        "a": "b",
        "c": "d",
        "e": "f"
      },
      "string": "Hello World"
    }
    #print(jsonData)
    #return jsonData["array"][0]
    #return render_template('temperature.html')
    session['data'] = data5.tolist()
    import csv
    csv.register_dialect(
       'mydialect',
       delimiter = ',',
       quotechar = '"',
       doublequote = True,
       skipinitialspace = True,
       lineterminator = '\r\n',
       quoting = csv.QUOTE_MINIMAL)
    
    with open('mydata1.csv', 'w') as mycsvfile:
       thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
       for row in data5:
           thedatawriter.writerow(row)
    
    session['classification'] = jsonData["array"]
    count = 0
    for i in jsonData["array"]:
        if i==9:
            count+=1
    print(count)

    if count>15:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
         
         
        fromaddr = "archhacks0511@gmail.com"
        toaddr = "venkatanarendra18@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Notification regarding patient Mike"

        print("Anomaly with the data samples, A Notification has been sent to Doctor")
        print(" Visit this link : http://localhost:5000 to get more info.");
        body = "Pateint Mike has anomaly, Kindly check this : http://localhost:5000/records"
        msg.attach(MIMEText(body, 'plain'))
         
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(fromaddr, "ufatarchhacks")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

    
    return render_template('dashboard.html')
@app.route('/dashboard')
def index():
    return render_template('dashboard.html')
@app.route('/records')
def index2():
    return render_template('records.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/emergency')
def emergency():
    return render_template('emergency.html')

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')


@app.route('/data2')
def data2():
    return render_template('data2.html')


@app.route('/data3')
def data3():
    return render_template('data3.html')


@app.route('/data4')
def data4():
    return render_template('data4.html')


if __name__ == '__main__':
    app.run(debug=True)
