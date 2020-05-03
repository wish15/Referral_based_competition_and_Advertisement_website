
# Referral_based_competition_and_Advertisement_website 

This website is built using python flask and Mongodb. This website is for the advertisement of a product, 
The idea is to build a simple competition webpage within the client’s website that encourages people to spread the news about the new product.
Users arrive at the page and sign up a form. After a successful sign up, they get one entry for the competition. 
At that point, they also have an option to share the sign-up link. Every successful sign up referred via the link will give extra competition entries to the original link poster.
There is no limit to the number of entries that a person can have. So, the idea is: The more entries you have, the higher your chance to win the prize. 

# Getting started

clone the repository by using the following command

```
  $ git clone https://github.com/wish15/Referral_based_competition_and_Advertisement_website.git
```


After cloning go to the directory of the project
and then run following command to install all the libraries.

```
 $ pip install -r requirements.txt
```
After installing all the dependencies open app.py file and write the senders email_id and password to send the mail to all the contestants after signing.
Make sure you have given permission two less secure apps if not click this link and toggle the permission https://myaccount.google.com/lesssecureapps

Now start the server by running,
```
 $ python app.py 
```

Open the localhost in the browser at port 5000 i.e. http://127.0.0.1:5000

You will see the home page of the website with content and information about the product and a leaders board and a from to know you referral counts
Now click on signin button on the navbar on the top
Fill the correct information and for the first time leave the referral code field empty
You will be redirected to the home page of the website and you will receive a mail which contains your referral code and
the mail also contains two links by clicking you will have an option to post a special link to the competition page containing your referral code in facebook/tweeter
ones your friend clicks the special link you have tweeted he will be redirected to the contest registration page and in signup for referral code field will be filled with your referral code automatically
when your friend signup using your referral your count of referrals will get updated in database.
The leaders-board will display the top 10 contestants with their referral counts.
You can see your referral count by entering your email id and name in form given in home page.
If during registration you left a field unfilled except referral code field or you entered a email or contact info which already exists in db then corresponding error message will be displayed 
