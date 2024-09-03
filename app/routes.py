from flask import render_template, request, redirect, url_for, flash, session, jsonify, abort
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import BlogPost, Project
from .forms import BlogPostForm, ProjectForm
import logging
import os
from werkzeug.utils import secure_filename


def init_routes(app):
    app.secret_key = os.environ.get('SECRET_KEY', 'mysecret')
    app.config['UPLOAD_FOLDER'] = 'app/static/images'

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/blogs')
    def blogs():
        try:
            entries = BlogPost.get_blog_entries()
            logging.info(f'Fetched {len(entries)} blog entries')
        except Exception as e:
            logging.error(f'Error fetching blog entries: {e}')
            entries = []
        return render_template('blog.html', entries=entries)

    @app.route('/blog/<int:entry_id>')
    def blog_entry(entry_id):
        entry = BlogPost.get_blog_entry(entry_id)
        if not entry:
            abort(404, description="Resource not found")
        return render_template('blog_entry.html', entry=entry)



    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username == os.environ.get('ADMIN_USERNAME') and password == os.environ.get('ADMIN_PASSWORD'):
                session['logged_in'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password. Please try again.')
        return render_template('admin_login.html')

    @app.route('/admin/dashboard')
    def admin_dashboard():
        if not session.get('logged_in'):
            flash('You need to log in first.')
            return redirect(url_for('admin_login'))
        return render_template('admin_dashboard.html')

    @app.route('/admin/manage')
    def manage():
        if not session.get('logged_in'):
            flash('You need to log in first.')
            return redirect(url_for('admin_login'))
        return 'This will be the manage page.'

    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        flash('You have been logged out.')
        return redirect(url_for('home'))
    
    @app.route('/admin/create-post', methods=['GET', 'POST'])
    @app.route('/admin/edit-post/<int:post_id>', methods=['GET', 'POST'])
    def create_or_edit_post(post_id=None):
        post = BlogPost.query.get(post_id) if post_id else None
        form = BlogPostForm(obj=post)
        if form.validate_on_submit():
            filename = None
            if 'image' in request.files:
                image = request.files['image']
                if image and image.filename:
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            tags_list = request.form.getlist('tags[]')
            tags_string = ', '.join(tags.strip() for tags in tags_list if tags.strip())

            if post:
                post.title = form.title.data
                post.description = form.description.data
                post.tags = tags_string
                post.body = form.body.data
                if filename:
                    post.image = filename
                db.session.commit()
                flash('Your post has been updated!', 'success')
            else:
                post = BlogPost(
                    title=form.title.data,
                    description=form.description.data,
                    tags=tags_string,
                    body=form.body.data,
                    image=filename
                )
                db.session.add(post)
                db.session.commit()
                flash('Your post has been created!', 'success')

            return redirect(url_for('home'))

        return render_template('create_post.html', title='Edit Post' if post_id else 'New Post', form=form, post=post)

    @app.route('/admin/delete-post/<int:post_id>', methods=['POST'])
    def delete_post(post_id):
        post = BlogPost.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('The post has been deleted.', 'success')
        return redirect(url_for('blogs'))

    @app.route('/filter-blogs')
    def filter_blogs():
        tag = request.args.get('tag')
        page = request.args.get('page', 1, type=int)
        per_page = 6
        try:
            entries = BlogPost.get_blog_entries(tag=tag, page=page, per_page=per_page)
            logging.info(f'Fetched {len(entries)} blog entries')
        except Exception as e:
            logging.error(f'Error fetching blog entries: {e}')
            entries = []
        return render_template('blog.html', entries=entries)

    @app.route('/blog-post/<int:post_id>')
    def blog_post(post_id):
        post = BlogPost.query.get_or_404(post_id)
        return render_template('blog_post.html', title=post.title, post=post)

    @app.route('/projects')
    def view_projects():
        projects = Project.query.all()
        categories = {project.category for project in projects}
        return render_template('projects.html', projects=projects, categories=categories)

    @app.route('/manage/projects', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def manage_projects():
        form = ProjectForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                file = request.files['image']
                filename = None
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    image_url = url_for('static', filename='images/projects/' + filename)
                else:
                    image_url = None

                new_project = Project(
                    title=form.title.data,
                    description=form.description.data,
                    category=form.category.data,
                    technologies=form.technologies.data,
                    image=image_url
                )
                db.session.add(new_project)
                db.session.commit()
                flash('Project added successfully!', 'success')
                return redirect(url_for('view_projects'))

        elif request.method == 'PUT':
            project_id = request.args.get('id')
            project = Project.query.get(project_id)
            if project:
                if form.validate_on_submit():
                    project.title = form.title.data
                    project.description = form.description.data
                    project.category = form.category.data
                    project.technologies = form.technologies.data

                    file = request.files['image']
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(file_path)
                        project.image = url_for('static', filename='images/projects/' + filename)

                    db.session.commit()
                    flash('Project updated successfully!', 'success')
                    return jsonify({'message': 'Project updated'}), 200
                else:
                    return jsonify({'errors': form.errors}), 400
            else:
                return jsonify({'message': 'Project not found'}), 404

        elif request.method == 'DELETE':
            project_id = request.args.get('id')
            project = Project.query.get(project_id)
            if project:
                db.session.delete(project)
                db.session.commit()
                flash('Project deleted successfully!', 'success')
                return jsonify({'message': 'Project deleted'}), 200
            else:
                return jsonify({'message': 'Project not found'}), 404

        projects = Project.query.all()
        return render_template('add_projects.html', form=form, projects=projects)

    @app.route('/projects/<int:id>')
    def project_detail(id):
        project = Project.query.get_or_404(id)
        return render_template('project_detail.html', project=project)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
