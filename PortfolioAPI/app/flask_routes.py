"""Routes for our flask app"""
from flask import request
from .data_loader import DataLoader
from . import app
#Flask Routes

#Set Up Data stuff
loader = DataLoader()
#GET

@app.get("/resume")
def resume():
    """Gets whole resume"""
    return {"resume": ["ContactInto","Coursework","Education","Languages","Projects","WorkExperience"]},200

@app.get("/")
def hello():
    return "Hi, welcome to my API Resume, you can head to /resume to see the different categories, or /resume/categoryname to look at a specific one, you can also go to /comment to find out how to leave a comment"
    
@app.get("/resume/<resume_type>")
def get_resume_type(resume_type,loader = loader):
    """Gets specific type from resume"""
    try:
        resume = loader.load(resume_type)
        return resume, 200
    except Exception:
        return "", 404


@app.get("/comments")
def get_comment_form():
    """look into adding a new comment"""
    return "You can POST a json here to send me a comment if you'd like :)"

#POST

@app.post("/comments")
def post_comment(current_loader=loader):
    """Post a new Comment"""
    comment = request.get_json(force=True)
    comment["ip"] = request.remote_addr
    loader.write(comment)
    return "", 202
    
    
