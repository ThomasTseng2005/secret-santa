from flask import Flask
from flask import render_template, redirect, url_for, request
import random
from models import SecretSanta
import smtplib
import email.utils
from email.mime.text import MIMEText

app = Flask(__name__)
secretsanta = SecretSanta()
server = smtplib.SMTP("smtp.gmail.com",587)
username = "secretsantaoverlord1225@gmail.com"
password = "christmas1225"


@app.route('/',  methods=['GET', 'POST'])
def start():
    if request.method == "POST":
        number = request.form["playernumber"]
        secretsanta.messagetwo = ""
        if number.isdigit() == True:
            number = int(number)
            if number > 1 and number <= 50:
                secretsanta.people = number
                return redirect(url_for("next"))
            else:
                secretsanta.message = "Please type in a number from 2-50!"
        else:
            secretsanta.message = "Please type in a number from 2-50!"

    return render_template("start.html", message = secretsanta.message)

@app.route('/setup', methods=['GET', 'POST'])
def next():
    secretsanta.player_list = []
    secretsanta.email_list = []
    if request.method == "POST":
        location = request.form["location"].title()
        date = request.form["date"]
        max = request.form["maxprice"]
        min = request.form["minprice"]
        player_list = request.form.getlist("names")
        email_list = request.form.getlist("emails")
        count = len(player_list)
        if location == "" or date == "" or max == "" or min == "":
            secretsanta.messagetwo = "Please fill in all the textfields and no repeated names!"
            return render_template("continue.html", message=secretsanta.messagetwo, number=secretsanta.people)
        if max.isdigit() == False or min.isdigit() == False:
            secretsanta.messagetwo = "Please fill in all the textfields and make sure the prices are integers above 0!"
            return render_template("continue.html", message=secretsanta.messagetwo, number=secretsanta.people)
        max = int(max)
        min = int(min)
        if max < min or max <= 0 or min <= 0:
            secretsanta.messagetwo = "Please fill in all the textfields and make sure that the maximum price is greater than the minimum price!"
            return render_template("continue.html", message=secretsanta.messagetwo, number=secretsanta.people)
        for i in player_list:
            if i != "" and player_list.count(i) == 1:
                i.strip()
                i.title()
                secretsanta.player_list.append(i)
            else:
                secretsanta.messagetwo = "Please fill in all the textfields and no repeated names!"
                return render_template("continue.html", message=secretsanta.messagetwo, number=secretsanta.people)
        for a in email_list:
            if a != "":
                secretsanta.email_list.append(a)
            else:
                secretsanta.messagetwo = "Please fill in all the textfields and valid emails!"
                return render_template("continue.html", message=secretsanta.messagetwo, number=secretsanta.people)
        secretsanta.random_list = random.sample(secretsanta.player_list, len(secretsanta.player_list))
        print(secretsanta.random_list)
        while count > 0:
            for person in secretsanta.player_list:
                if secretsanta.player_list.index(person) == secretsanta.random_list.index(person):
                    secretsanta.random_list = random.sample(secretsanta.player_list, len(secretsanta.player_list))
                    count = len(secretsanta.player_list)
                    print(count)
                    break
                else:
                    count -= 1
                    print(count)
                    print("Good")
        for p in secretsanta.player_list:
            secretsanta.result[p] = secretsanta.random_list[player_list.index(p)]
        print(secretsanta.result)
        for e in secretsanta.player_list:
            secretsanta.emails[e] = secretsanta.email_list[player_list.index(e)]
        for t in secretsanta.player_list:
            try:
                to_email = secretsanta.emails[t]
                from_email = "secretsantaoverlord1225@gmail.com"
                message = 'Subject: {}\n\n{}'.format("Secret Santa", "Hello " + t + ",\n" + "   On " + str(date) + " at " + str(location) + ", " + "you will have to buy a gift at a price ranged from " + str(min) + "~" + str(max) + " for your Secret Santee." + "\n   You are the Secret Santa of: " + secretsanta.result[t] + "! Remeber to keep it a secret!\n\n" + "From the Secret Santa Overlord")
                server = smtplib.SMTP("smtp.gmail.com", 587)
                username = "secretsantaoverlord1225@gmail.com"
                password = "christmas1225"
                server.starttls()
                server.login(username, password)
                server.sendmail(from_email, to_email, message)
                server.quit()
            except:
                print("Doesn't work")


        return redirect(url_for("finish"))


    return render_template("continue.html", message=secretsanta.messagetwo, number=secretsanta.people)

@app.route('/finish', methods=['GET', 'POST'])
def finish():
    return render_template("finish.html")



if __name__ == '__main__':
    app.run(debug = True)
