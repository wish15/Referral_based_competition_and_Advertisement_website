import pymongo
from flask import Flask,flash,redirect,render_template,request
from flask_mail import Mail,Message

# flask app configuration for mail
app=Flask(__name__)
app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'vishalrochlanimh@gmail.com',
    MAIL_PASSWORD = 'Radhasoamiji@123'
    )
mail=Mail(app)

# mongo db configuration
client=pymongo.MongoClient("mongodb://127.0.0.1:27017")
user_db=client["honeymintdb"]
User_Collection=user_db["usersdb"]



# function to generate a new reffral code for new signup generation unique referral which contains users
# fisrtname and a unique number which is eqaul to count of entries in db followed by string -HM example: Vishal-15-HM
def generate_referral_code(first_name):
    count=len(list(User_Collection.find()))
    new_reffral_code=first_name+"-"+str(count)+"-HM"
    return new_reffral_code

# function to send mail through provided mail_id and password
def send_mail(username,referral,email):
    try:
        msg = Message("Honeymint!! Registation Complete",sender="vishalrochlanimh@gmail.com",recipients=[email])
        msg.html = render_template('register_mail.html', username=username,referral=referral)        
        mail.send(msg)
        return 'Mail sent'
    except Exception as e:
        print()
        return(str(e))


# Home page route
@app.route('/')
def home(msg=""):
    users=list(User_Collection.find().sort("referral_count",-1))
    if(len(users)>10):
        users=users[:10]
    return render_template('home.html',users=users,msg=msg)

#signup with referral route
@app.route('/signup/<string:referral>/')
def signup(referral,msg=""):
    return render_template('signup.html',referral=referral,msg=msg)

# signup without referral route
@app.route('/signup/')
def signup_without_referral(msg=""):
    return render_template('signup.html',msg=msg)

# about page route more information about product and competition
@app.route('/about')
def about():
    return render_template('about.html')

# route to know the count of persons signed in using your referral code
@app.route('/your_referrals',methods=['POST'])
def know_your_referals():
    current_user=str(request.form['name'])
    current_email=str(request.form['email'])
    user_in_db=User_Collection.find_one({'email':current_email})
    if(user_in_db):
        user_referral_code=user_in_db['referral_code']
        return render_template('referralcounts.html',name=current_user,referral_count=user_in_db['referral_count'],referral_code=user_referral_code)
    return home('email not found')


# user registration and updation in database
@app.route('/register',methods=['POST'])
def register():
    first_name=str(request.form['first_name'])
    last_name=str(request.form['last_name'])
    email=str(request.form['email'])
    address=str(request.form['address'])
    phone_no=str(request.form['phone_no'])
    referred_by=str(request.form['referral'])
    user_referral_code=generate_referral_code(first_name)
    current_email={'email':email}
    current_phone_no={'phone_no':phone_no}
    current_user=User_Collection.find(current_email)
    user_exists=len(list(current_user))
    new_user=dict()
    new_user['first_name']=first_name
    new_user['last_name']=last_name
    new_user['email']=email
    new_user['address']=address
    new_user['phone_no']=phone_no
    new_user['referral_code']=user_referral_code
    new_user['referred_by']=referred_by
    new_user['referral_count']=0
    for field in new_user:
        if(field!='referred_by' and new_user[field]==""):
            return signup(referred_by,'Please fill all the field only referral code field is optional')
    if user_exists:
        #flash()
        return signup(referred_by,"Email already exists")
    current_user=User_Collection.find(current_phone_no)
    user_exists=len(list(current_user))
    if(user_exists):
        return signup(referred_by,"Phone number alredy exists")
    referred_by_user=User_Collection.find_one({'referral_code':referred_by})
    if(referred_by_user):
        User_Collection.update({'referral_code':referred_by},{'$inc':{'referral_count':1}})
    elif(referred_by!=""):
        return signup_without_referral('Wrong referral code put right referral or leave it blank')
    User_Collection.insert_one(new_user)
    send_mail(first_name,user_referral_code,email)
    return home()

if __name__ == "__main__":
    app.run(debug=True)