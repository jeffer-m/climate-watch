# # seed.py
# from application import create_app
# from application.extensions import db
# from application.models import Post

# app = create_app()

# with app.app_context():
#     db.create_all()

#     if Post.query.count() == 0:
#         post1 = Post(title="Welcome!", content="This is the first system post.", user_id=1)
#         post2 = Post(title="Info", content="Please register to post.", user_id=1)
#         db.session.add_all([post1, post2])
#         db.session.commit()
#         print("Initial posts seeded.")
#     else:
#         print("Posts already exist.")




# #routes.py
# from flask import Flask, render_template, Blueprint, jsonify, request, flash, redirect, url_for
# from .api_utils import get_climate_data, get_climate_news,get_weather_data,get_coordinates
# from flask_login import login_required,current_user,login_user
# from application.models import db,Post, User

# import joblib
# from flask import request, render_template
# # from application import app  # Removed, app should be imported and blueprint registered in the main application file


# routes = Blueprint('routes', __name__)

# @routes.route("/", methods=['GET', 'POST'])
# def index():
#     location = request.form.get('location') or request.args.get('location')
#     lat = None
#     lon = None
    
#     if location:
#         coords = get_coordinates(location)
#         if coords:
#             lat, lon = coords
    
#     weather_data = get_weather_data(lat, lon)
#     climate_data = get_climate_data(lat, lon)

#     # Handle empty climate data
#     if not climate_data or "trend_years" not in climate_data:
#         climate_data = {
#             "trend_years": list(range(1990, 2021)),
#             "trend_values": [25 + (i * 0.1) for i in range(31)],
#             "min_temps": [24 + (i * 0.1) for i in range(31)],
#             "rainfall": [100 + i * 5 for i in range(31)],
#             "coordinates": {"latitude": lat, "longitude": lon} if lat and lon else None
#         }

#     return render_template(
#         "index.html",
#         weather=weather_data,
#         trend_years=climate_data["trend_years"],
#         max_temps=climate_data["trend_values"],
#         min_temps=climate_data["min_temps"],
#         rainfall=climate_data["rainfall"],
#         location=location,
#         coordinates=climate_data.get("coordinates")
#     )

# @routes.route('/climate-news')
# def climate_news():
#     # Serve first page
#     articles,next_page = get_climate_news()
#     return render_template('climate-news.html', articles=articles,next_page=next_page)


# @routes.route('/load-news')
# def load_news():
#     next_page = request.args.get('nextPage', type=int)
#     articles, new_next_page = get_climate_news(next_page)

#     html = render_template("news_fragment.html", articles=articles)
#     return jsonify({
#         "html": html,
#         "next_page": new_next_page
#     })

# @routes.route('/climate-art')
# def climate_art():
#     posts= Post.query.order_by(Post.date_created.desc()).all()
#     return render_template('climate-art.html', posts = posts)

# @routes.route('/create', methods = ['GET','POST'])

# def create_post():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         post = Post(title=title,content=content,author = current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash("Post created")
#         return redirect(url_for('main.index'))
#     return render_template('create_post.html')



# @routes.route('/climate-oracle')
# @login_required
# def climate_oracle():
#     return render_template('climate-oracle.html')



# @routes.route('/login', methods=['GET', 'POST'])
# def login():
#     next_page = request.args.get('next')  # get the next destination

#     if request.method == 'POST':
#         action = request.form.get('action')
#         username = request.form['username']
#         password = request.form['password']

#         if action == 'login':
#             user = User.query.filter_by(username=username).first()
#             if user and user.check_password(password):
#                 login_user(user)
#                 flash("Welcome back!", "success")
#                 return redirect(next_page or url_for('routes.index'))

#             flash("Invalid credentials", "danger")

#         elif action == 'register':
#             existing_user = User.query.filter_by(username=username).first()
#             if existing_user:
#                 flash("Username already exists", "warning")
#             else:
#                 new_user = User(username=username)
#                 new_user.set_password(password)
#                 db.session.add(new_user)
#                 db.session.commit()
#                 login_user(new_user)
#                 flash("Registered and logged in!", "success")
#                 return redirect(next_page or url_for('routes.index'))

#     return render_template('login.html')




# @routes.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         # Check if user exists
#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             flash('Username already taken', 'warning')
#             return redirect(url_for('routes.register'))

#         # Create user
#         user = User(username=username)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Registration successful! You can now log in.', 'success')
#         return redirect(url_for('routes.climate_oracle'))

#     return render_template('register.html')


# from flask_login import logout_user

# @routes.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash("Logged out successfully", "info")
#     return redirect(url_for('routes.login'))

