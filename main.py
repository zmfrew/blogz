from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyNewPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(100000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

def input_error(input):
    if input == "":
        return  True
    else:
        return False

@app.route('/')
def reroute():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def index():

    blog_id = request.args.get('id')
    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('blog_display.html',title="Blog Post",blog=blog)


    blogs = Blog.query.filter_by().order_by(Blog.id.desc()).all()
    return render_template('blog.html',title="build-a-blog", 
        blogs=blogs)

@app.route('/blog?id={{blog.id}}', methods=['POST', 'GET'])
def display_blog():
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']

    return render_template('blog_display.html',title=blog_title,blog_body=blog_body)


@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():

    title_error = ""
    body_error = ""

    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']
        new_blog = Blog(blog_title, blog_body)

        if input_error(blog_title):
            title_error = "Please fill in the title"
        
        if input_error(blog_body):
            body_error = "Please fill in the body"

        if not input_error(blog_title) and not input_error(blog_body):
            db.session.add(new_blog)
            db.session.commit()
            new_blog_page = "/blog?id=" + str(new_blog.id)
            return redirect(new_blog_page)
            #return redirect('/blog')

    return render_template('newpost.html', title="Add a Blog Entry", title_error=title_error, body_error=body_error)


if __name__ == '__main__':
    app.run()