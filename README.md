#goal_flask_app

A goal or to-do list web app using the Flask web framework and a MySQL backend. It is fully functional, but has plenty of room for feature growth.

This code can be run on your own webserver, but was originally developed for PythonAnywhere. Because of that, this guide will give info on how to deploy the code there.


##Deployment/Installation Instructions

1. If you don’t have an account already, setup a free account with http://PythonAnywhere.com
2. Choose “I want to create a web app”
3. Go to the “Web” tab and then to the “Add a new web app” to the left.
4. Click next until you get the page asking for framework. Choose “Flask”.
5. Then choose Flask for Python 2.7 (that’s what the goal code works with).
6. Then click next and finish up.
7. When you go to your URL (username.pythonanywhere.com) you should see a message “Hello from Flask!” That means you’re doing well so far :)
7. Next go to the “Databases” tab. We’re going to setup some databases for the site.
8. Create a MySQL password. Make sure to remember it or write it down.
9. Now create two databases: “goallist” and “goallistusers”.
10. Start a console on “goalist” and use “dbschema/create_goals.sql” to create the “goals” table.
11. Start a console on “goallistusers” and use “dbschema/create_users.sql” to create the “users” table.
12. Open flask_app.py and change user and passwd fields (this needs to be separated). Make sure to add “username$” to the front of each tablename (e.g. “goallist” should be “username$goallist” where username is your pythonanywhere username). Also, change “SECRET KEY” to some randomly generated string, for safety.
13. Next go to the “Files” tab and select the “mysite” folder.
14. Upload all files.
15. Go to the “Web” tab and reload your website.
16. Check out your site and see if you get the login page.
17. Next create a user by going back to the console for “goallistusers” and running something like:
```INSERT INTO users (username, password, email) VALUES (‘username’, md5(‘password’), ‘email’)```
18. Make sure to use md5 on the password (although you might want to strengthen this) and make sure to change ‘username’, ‘password’ and ‘email’ to whatever you’d like.
19. Make sure to log out of the consoles (having two open will prevent you from logging in under the free account).
20. Now go back to the login window and insert the username and password.
21. If you have any problems:
  * go to the “Web” tab and check error log.
  * make sure to check that all of the database schema was applied (login to the MySQL consoles and run “DESCRIBE goals” or “DESCRIBE users”). If they don’t match the .sql files, then add the necessary info. 
  * check that all user/passwd for MySQL connections were updated to your user/passwd and that you added “username$” to the front of the database as described in step 13.
  * check text encoding and try directly editing and pasting into “flask_app.py”.
  * Make sure you reloaded your web app.
