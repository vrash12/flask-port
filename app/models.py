#app/models.py
from . import db
from datetime import datetime
import logging

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200))
    body = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlogPost "{self.title}">'
    
    @classmethod
    def get_blog_entry(cls, id):
        try:
            return cls.query.get(id)
        except Exception as e:
            logging.error(f'Error in get_blog_entry: {e}')
            return None

    @classmethod
    def get_blog_entries(cls):
        try:
            return cls.query.all()
        except Exception as e:
            logging.error(f'Error in get_blog_entries: {e}')
            return []




class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)  # A new field to categorize projects
    technologies = db.Column(db.String(200))  # Comma-separated list of technologies used
    image = db.Column(db.String(300))  # Path to project image
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Project "{self.title}">'

    @classmethod
    def get_project(cls, id):
        try:
            return cls.query.get(id)
        except Exception as e:
            logging.error(f'Error in get_project: {e}')
            return None

    @classmethod
    def get_projects(cls):
        try:
            return cls.query.all()
        except Exception as e:
            logging.error(f'Error in get_projects: {e}')
            return []