

from datetime import datetime
from email import contentmanager
from turtle import title
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from traitlets import default
from datetime import datetime

#base.html will contain all the html for the common part for all users, it is the base template
''' 
Blocks are used to reference those parts of the base.html, which
will be used differently by different parts, the different webpages inherit all the common
things from the base.html, process is called rendering templates
'''
app = Flask(__name__)

#set up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(30), default = "Anonymous")
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

          

    def __repr__(self):
        return "BLOG POST" + str(self.id)



#templates are used for displaying the front end part
# / is for the base directory or the index.html
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/posts', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        #new_post BlogPost(title = post_title, content=post_content, author = po)
        new_post = BlogPost(title = post_title, content = post_content, author = post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('\posts')
        
        
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts = all_posts)

#this routes the url to whatever/home/users/name_in_url/posts/id_in_url
@app.route("/home/users/<string:name>/posts/<int:id>")
def hello(name, id):
    return "Hello, " + name + " with id = " + str(id)

#GET is used to request data from a particular server/ application
#POST is used to send data to a server to create/update a resource
@app.route("/only_get", methods = ["GET","POST"])
def get():
    return "You can only get this webpage"


@app.route("/posts/delete/<int:id>")
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("\posts")

@app.route("/posts/edit/<int:id>", methods = ["GET", "POST"])
def edit(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == "POST":
        
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect("\posts")
    else:
        return render_template("edit.html", post = post)



if __name__ == "__main__":
    app.run(debug=True)