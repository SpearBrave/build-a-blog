from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"]= "mysql+pymysql://build-a-blog:bbb@localhost:3306/build-a-blog"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

class Blog(db.Model): # blog.name blog.body comes from this

    id =   db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(300))
 
    def __init__(self, name,body):
        
        self.name = name
        self.body = body
    


@app.route("/blog" )
def index ():
    blog_id = request.args.get("id")  #gets id number
    if blog_id :
        single = Blog.query.get(blog_id)
        return render_template("new_blog.html",blog=single) #uses single blogs info
    blogs = Blog.query.all()
    

    return render_template("todos.html",blogs=blogs)


@app.route("/new_post",methods=["POST","GET"])
def new_post():
    if request.method == "POST": 
        Title = request.form["Title"] #takes the input from form.html   #*** line 52 ***
        Body = request.form["body"]   # same                            #*** line 52 *
        errorTitle= ""
        errorBody= ""

        if Title == "" :
            errorTitle = "error no chracters"
    
        if Body == "":
            errorBody= "error no characters"
        if errorTitle or errorBody :
            return render_template("forms.html", errorTitle=errorTitle,errorBody=errorBody)
    
        new_blog = Blog(Title,Body)  
        db.session.add(new_blog)    #  git bash
        db.session.commit()            
        blog_id= new_blog.id #takes the blogs id 
    
        return redirect("/blog?id="+str(blog_id)) # adds the link to the blog_id with concatenation
    return render_template("forms.html")



if __name__ == "__main__":
    app.run()



