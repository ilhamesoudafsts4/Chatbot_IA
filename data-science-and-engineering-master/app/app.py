
from flask import Flask ,request,render_template ,redirect, url_for,flash,current_app,send_from_directory, session,jsonify
import os
from bson import ObjectId
from werkzeug.utils import secure_filename
from functions import *
from config import Config
from  flask_mail  import  Message ,Mail
from os.path import join, dirname, realpath
import datetime
import time
from flask_mysqldb import MySQLdb
import re
import requests
from flask import Markup
import json
# import urllib library
import urllib.request 
from slugify import slugify

# import json
import json
now = datetime.datetime.now()
app=Flask(__name__,template_folder='Template')

conn= MySQLdb.connect (host = "localhost", user = "root", passwd = "",db="chatbot")

cursor = conn.cursor()








app.config.from_object(Config)
mail = Mail(app)
#cursor = conn.cursor()
#cursor.execute("CREATE TABLE condidature(id INT NOT NULL PRIMARY KEY, nom varchar(200),Prenom varchar(200), email varchar(200),Tele varchar(200),Adresse varchar(200),files varchar(200),descp varchar(200))")
#conn.commit()
#cursor.close()


UPLOAD_FOLDER = UPLOADS_PATH = join(dirname(realpath(__file__)),'static1/uploads/..')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  
ALLOWED_EXTENSIONS = set(['pdf', 'docx'])
   
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  

#la permiére vu de chatbot
@app.route('/')
@app.route('/chatbot', methods=['GET', 'POST'])
def welcome():
    return render_template('index.html')





@app.route('/predect', methods=['GET', 'POST'])
def get_predection():
       data= request.get_json()
       
       print(data)
       time_of_day = time.strftime(' %H:%M', time.localtime())
       time_of_day2 = time.strftime('%d/%m/%y ', time.localtime())
   
       res = predict_class(data)
       print(res)
       #engine = pyttsx3.init()
       #engine.say(res)
       #engine.runAndWait()
       #engine.setProperty('volume',.5)
       if res=="profil":
            boldtext = Markup("<a href='http://127.0.0.1:5000/login'>Bienvenu je vous invite de cliquer sur ce lien</a>")
            cover= boldtext
            
            return jsonify({"message":cover} )
       if data=="je voulais postuler à un condidat spantané":
             boldtext = Markup("<a href='http://127.0.0.1:5000/spantane/'>Condidature spantané remplir cette formulaire</a>")
             cover= boldtext
             return jsonify({"message":cover})
       if res=="vous voulez un rendez-vous":
            boldtexte = Markup("<a href='http://127.0.0.1:5000/RDV'>Veuillez Consulter le planing de la socièté et reservez un créneaux convenable</a>")
            cover= boldtexte
            return jsonify({"message":cover})
       if res=="partenariat":
            boldtexte = Markup("<a href='http://127.0.0.1:5000/partenariat'>Bienvenu nous invite à remplir certains informations</a>")
            cover= boldtexte
            return jsonify({"message":cover})    
       #if res=="i cann't undarstant you":
       #res='you can complain about your problem'
            # return render_template('index_from.html',response=res,mes=data,time=time_of_day,time2=time_of_day2 )
       else:
              return jsonify({"message":res})
 
@app.route('/spantane/', methods=['GET', 'POST'])
def spantane():
    return render_template('condidature_spantane.html')


@app.route('/condidature/', methods=['GET', 'POST'])
def sen_recal():
            
            if request.method=='POST':
               nom=request.form['nom']
               
               email=request.form['email']
               Tele=request.form['Tele']
               Adresse=request.form['ville']
               files = request.files.getlist('files[]')
               
               for file in files:
                  if file and allowed_file(file.filename):
                     files = secure_filename(file.filename)
                     file.save(os.path.join(app.config['UPLOAD_FOLDER'], files))
              
               cursor = conn.cursor()    
               cursor.execute('''INSERT INTO  condidat VALUES(%s,%s, %s, %s,%s)''',(nom, email,Tele,Adresse,files))
               conn.commit()
               cursor.close()
               
                            
            
            flash('votre condidature a été envoyé')
            return render_template('index.html')
            


#Répondre au condidature espace admin
#@app.route ( "/send" ,methods=['GET', 'POST']) 
#def  send (): 
    #cursor = conn.cursor()   
   
    #cursor.execute("SELECT  email FROM  condidat WHERE nom='ilhame';")
    #to=cursor.fetchall()
    #conn.commit()
    #cursor.close()
    #to=' '.join(map(str,to))
    #print(to)
    #reclamation=request.form['Reclamation']
    #Soltution=request.form['Solution']
    #msg  =  Message ( "Réclamation" , 
                 
                  #recipients = [to])
    #msg.body = "votre probleme est en cours de traitement "
    #msg.html = Soltution
    #mail.send(msg)
    #return render_template('admin.html')


#affichage des informations de condidat espace admin
@app.route('/renvoie')
def renvoie():
   cursor = conn.cursor()  
   
   cursor.execute("SELECT nom, email,Tele,Adresse,files FROM condidat;")
   to=cursor.fetchall()
   conn.commit()
   cursor.close()
   print(to)
   return render_template('admin.html',response=to)

 #técharger CV
@app.route('/static/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'] )
    return send_from_directory(directory=uploads, path=filename,as_attachment=True)





  

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM utilisateur WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            #session['userid'] = user['userid']
            #session['name'] = user['name']
            #session['email'] = user['email']
            #mesage = 'Logged in successfully !'
            return render_template('condidature_profil.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)




@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['username']
       
        email = request.form['email']
        password = request.form['password']
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM utilisateur WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO utilisateur VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            conn.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('login.html', mesage = mesage)








from authlib.flask.client import OAuth

oauth = OAuth(app)

app.config['SECRET_KEY'] = "THIS SHOULD BE SECRET"
app.config['GOOGLE_CLIENT_ID'] = "544409459410-soi2jt7c7sc3jdf8rc2mb32e3sp8jujb.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"
app.config['GITHUB_CLIENT_ID'] = "4a2a5485744a95c98aea"
app.config['GITHUB_CLIENT_SECRET'] = "47787183fbf1ff21b62678544b7f1038bdced231"

google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)



github = oauth.register (
  name = 'github',
    client_id = app.config["GITHUB_CLIENT_ID"],
    client_secret = app.config["GITHUB_CLIENT_SECRET"],
    access_token_url = 'https://github.com/login/oauth/access_token',
    access_token_params = None,
    authorize_url = 'https://github.com/login/oauth/authorize',
    authorize_params = None,
    api_base_url = 'https://api.github.com/',
    client_kwargs = {'scope': 'user:email'},
)

# Github login route
@app.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


# Github authorize route
@app.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()
    print(f"\n{resp}\n")
    return  render_template('condidature_profil.html')



# Default route
@app.route('/')
def index():
  return render_template('index.html')


# Google login route
@app.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    print(f"\n{resp}\n")
    return render_template('condidature_profil.html')




#RDV CANDIDAT
@app.route('/RDVCandidat', methods =['GET', 'POST'])
def RDVCandidat():
    secuss = ''
    if request.method == 'POST':
        if request.form['submit_button'] == 'Lundi10':
            
            nom = request.form['namecndl10']
            prenom = request.form['prenomcndl10']
            date = request.form['datecndl10']
            datem = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M")
            email = request.form['emailcndl10']
            tele = request.form['telecndl10']
            

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM rdvcandidat WHERE date = %s', (date, ))
            rdv = cursor.fetchone()
            if rdv:
                flash("RDV déjà réserver remplir un autre !")
            elif datem.hour!=10 or datem.minute!=00:
                flash("Veuillez saisir un crénaux valide: 10h00 ")
            elif  datem.strftime('%A') != "Monday" :
                flash("Veuillez saisir un jour valide : Lundi!")
            # elif current_date.year > datem.year and current_date.month > datem.month and current_date.day > datem.day and current_date.hour > datem.hour and current_date.minute > datem.minute:
            #     mesage ="Veuillez saisir une date supèrier de ce moment"
            elif now > datem :
                flash("Veuillez saisir un date supérieur de ce moment !")
            else:
                cursor.execute("insert into rdvcandidat(nom,prenom,date,email,tele)values(%s,%s,%s,%s,%s)",(nom,prenom,date,email,tele))
                conn.commit()
            
                cursor.close()
                secuss = datem
                flash(secuss)
        elif request.form['submit_button'] == 'Lundi16':
            nom = request.form['namecndl16']
            prenom = request.form['prenomcndl16']
            date = request.form['datecndl16']
            datem = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M")
            email = request.form['emailcndl16']
            tele = request.form['telecndl16']

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM rdvcandidat WHERE date = %s', (date, ))
            rdv = cursor.fetchone()
            if rdv:
                flash("RDV déjà réserver remplir un autre !")
            elif datem.hour!=16 or datem.minute!=00:
                flash("Veuillez saisir un crénaux valide: 16h00!")
            elif datem.strftime('%A') != "Monday" :
                flash("Veuillez saisir un jour valid : Lundi !")
            # elif current_date.year > datem.year and current_date.month > datem.month and current_date.day > datem.day and current_date.hour > datem.hour and current_date.minute > datem.minute:
            #     mesage ="Veuillez saisir une date supèrier de ce moment"
            elif now > datem :
                flash("Veuillez saisir un date supérieur de ce moment !")
            else:
                cursor.execute("insert into rdvcandidat(nom,prenom,date,email,tele)values(%s,%s,%s,%s,%s)",(nom,prenom,date,email,tele))
                conn.commit()
            
                cursor.close()
                secuss = datem
                flash(secuss)
        elif request.form['submit_button'] == 'Mercredi10':
            nom = request.form['namecndm10']
            prenom = request.form['prenomcndm10']
            date = request.form['datecndm10']
            datem = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M")
            email = request.form['emailcndm10']
            tele = request.form['telecndm10']

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM rdvcandidat WHERE date = %s', (date, ))
            rdv = cursor.fetchone()
            if rdv:
                flash("RDV déjà réserver remplir un autre !")
            elif datem.hour!=10 or datem.minute!=00:
                flash("Veuillez saisir un crénaux valide: 10h00!")
            elif datem.strftime('%A') != "Wednesday" :
                flash("Veuillez saisir un jour valid : Mercredi !")
            # elif current_date.year > datem.year and current_date.month > datem.month and current_date.day > datem.day and current_date.hour > datem.hour and current_date.minute > datem.minute:
            #     mesage ="Veuillez saisir une date supèrier de ce moment"
            elif now > datem :
                flash("Veuillez saisir un date supérieur de ce moment !")
            else:
                cursor.execute("insert into rdvcandidat(nom,prenom,date,email,tele)values(%s,%s,%s,%s,%s)",(nom,prenom,date,email,tele))
                conn.commit()
            
                cursor.close()
                secuss = datem
                flash(secuss)
        else: 
            nom = request.form['namecndm16']
            prenom = request.form['prenomcndm16']
            date = request.form['datecndm16']
            datem = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M")
            email = request.form['emailcndm16']
            tele = request.form['telecndm16']

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM rdvcandidat WHERE date = %s', (date, ))
            rdv = cursor.fetchone()
            if rdv:
                flash("RDV déjà réserver remplir un autre !")
            elif datem.hour!=16 or datem.minute!=00:
                flash("Veuillez saisir un crénaux valide: 16h00!")
            elif datem.strftime('%A') != "Wednesday" :
                flash("Veuillez saisir un jour valid : Mercredi !")
            # elif current_date.year > datem.year and current_date.month > datem.month and current_date.day > datem.day and current_date.hour > datem.hour and current_date.minute > datem.minute:
            #     mesage ="Veuillez saisir une date supèrier de ce moment"
            elif now > datem :
                flash("Veuillez saisir un date supérieur de ce moment !")
            else:
                cursor.execute("insert into rdvcandidat(nom,prenom,date,email,tele)values(%s,%s,%s,%s,%s)",(nom,prenom,date,email,tele))
                conn.commit()
            
                cursor.close()
                secuss = datem
                flash(secuss)
    
    return render_template('planing.html', secuss= secuss )

#ROUTE RDV
@app.route('/RDV/')
def RDV():
    return render_template('planing.html')

@app.route('/partenariat')
def partenariat():
    return render_template('partenariat.html')


#RDV PARTENARIAT
@app.route('/RDVPart', methods =['GET', 'POST'])
def RDVPart():
    secuss = ''
    if request.method == 'POST':
        if request.form['submit_button'] == 'Lundi9':
            
            nom = request.form['nameprtl9']
            prenom = request.form['prenomprtl9']
            date = request.form['dateprtl9']
            datem = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M")
            email = request.form['emailprtl9']
            tele = request.form['teleprtl9']
            

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM rdvpartenariat WHERE date = %s', (date, ))
            rdv = cursor.fetchone()
            if rdv:
                flash("RDV déjà réserver remplir un autre !")
            elif datem.hour!=9 or datem.minute!=00:
                flash("Veuillez saisir un crénaux valide: 9h00 ")
            elif  datem.strftime('%A') != "Monday" :
                flash("Veuillez saisir un jour valide : Lundi!")
            # elif current_date.year > datem.year and current_date.month > datem.month and current_date.day > datem.day and current_date.hour > datem.hour and current_date.minute > datem.minute:
            #     mesage ="Veuillez saisir une date supèrier de ce moment"
            elif now > datem :
                flash("Veuillez saisir un date supérieur de ce moment !")
            else:
                cursor.execute("insert into rdvpartenariat(nom,prenom,date,email,tele)values(%s,%s,%s,%s,%s)",(nom,prenom,date,email,tele))
                conn.commit()
            
                cursor.close()
                secuss = datem
                flash(secuss)
        elif request.form['submit_button'] == 'Lundi11':
            nom = request.form['nameprtl11']
            prenom = request.form['prenomprtl11']
            date = request.form['dateprtl11']
            datem = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M")
            email = request.form['emailprtl11']
            tele = request.form['teleprtl11']

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM rdvpartenariat WHERE date = %s', (date, ))
            rdv = cursor.fetchone()
            if rdv:
                flash("RDV déjà réserver remplir un autre !")
            elif datem.hour!=11 or datem.minute!=00:
                flash("Veuillez saisir un crénaux valide: 11h00!")
            elif datem.strftime('%A') != "Monday" :
                flash("Veuillez saisir un jour valid : Lundi !")
            # elif current_date.year > datem.year and current_date.month > datem.month and current_date.day > datem.day and current_date.hour > datem.hour and current_date.minute > datem.minute:
            #     mesage ="Veuillez saisir une date supèrier de ce moment"
            elif now > datem :
                flash("Veuillez saisir un date supérieur de ce moment !")
            else:
                cursor.execute("insert into rdvpartenariat(nom,prenom,date,email,tele)values(%s,%s,%s,%s,%s)",(nom,prenom,date,email,tele))
                conn.commit()
            
                cursor.close()
                secuss = datem
                flash(secuss)
        elif request.form['submit_button'] == 'Mercredi9':
            nom = request.form['nameprtm9']
            prenom = request.form['prenomprtm9']
            date = request.form['dateprtm9']
            datem = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M")
            email = request.form['emailprtm9']
            tele = request.form['teleprtm9']

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM rdvpartenariat WHERE date = %s', (date, ))
            rdv = cursor.fetchone()
            if rdv:
                flash("RDV déjà réserver remplir un autre !")
            elif datem.hour!=9 or datem.minute!=00:
                flash("Veuillez saisir un crénaux valide: 9h00!")
            elif datem.strftime('%A') != "Wednesday" :
                flash("Veuillez saisir un jour valid : Mercredi !")
            # elif current_date.year > datem.year and current_date.month > datem.month and current_date.day > datem.day and current_date.hour > datem.hour and current_date.minute > datem.minute:
            #     mesage ="Veuillez saisir une date supèrier de ce moment"
            elif now > datem :
                flash("Veuillez saisir un date supérieur de ce moment !")
            else:
                cursor.execute("insert into rdvpartenariat(nom,prenom,date,email,tele)values(%s,%s,%s,%s,%s)",(nom,prenom,date,email,tele))
                conn.commit()
            
                cursor.close()
                secuss = datem
                flash(secuss)
        else: 
            nom = request.form['nameprtm11']
            prenom = request.form['prenomprtm11']
            date = request.form['dateprtm11']
            datem = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M")
            email = request.form['emailprtm11']
            tele = request.form['teleprtm11']

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM rdvpartenariat WHERE date = %s', (date, ))
            rdv = cursor.fetchone()
            if rdv:
                flash("RDV déjà réserver remplir un autre !")
            elif datem.hour!=11 or datem.minute!=00:
                flash("Veuillez saisir un crénaux valide: 11h00!")
            elif datem.strftime('%A') != "Wednesday" :
                flash("Veuillez saisir un jour valid : Mercredi !")
            # elif current_date.year > datem.year and current_date.month > datem.month and current_date.day > datem.day and current_date.hour > datem.hour and current_date.minute > datem.minute:
            #     mesage ="Veuillez saisir une date supèrier de ce moment"
            elif now > datem :
                flash("Veuillez saisir un date supérieur de ce moment !")
            else:
                cursor.execute("insert into rdvpartenariat(nom,prenom,date,email,tele)values(%s,%s,%s,%s,%s)",(nom,prenom,date,email,tele))
                conn.commit()
            
                cursor.close()
                secuss = datem
                flash(secuss)
    
    return render_template('planing.html', secuss= secuss )



    

#LISTE DES RENDEZ VOUS
@app.route("/IndexRDV")
def indexRDV():
    cursor = conn.cursor()
    cursor.execute("SELECT  * FROM rdvcandidat")
    rdvcnd = cursor.fetchall()
    cursor.execute("SELECT  * FROM rdvpartenariat")
    rdvprt = cursor.fetchall()
    cursor.close()
    
    return render_template("ListeRDV.html", rdvcnd=rdvcnd, rdvprt=rdvprt)













if __name__ == '__main__':
      app.secret_key = 'super secret key'
      app.config['SESSION_TYPE'] = 'filesystem'
      
      app.run(host='0.0.0.0',debug=True)