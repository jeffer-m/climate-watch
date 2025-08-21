
#routes.py
from flask import Flask, render_template, Blueprint, jsonify, request, flash, redirect, url_for
from .api_utils import get_climate_data, get_climate_news,get_weather_data,get_coordinates
from flask_login import login_required,current_user,login_user
from application.models import db,Post, User,check_password_hash

import joblib
from flask import request, render_template
# from application import app  # Removed, app should be imported and blueprint registered in the main application file


routes = Blueprint('routes', __name__)

@routes.route("/", methods=['GET', 'POST'])
def index():
    location = request.form.get('location') or request.args.get('location')
    lat = None
    lon = None
    
    if location:
        coords = get_coordinates(location)
        if coords:
            lat, lon = coords
    
    weather_data = get_weather_data(lat, lon)
    climate_data = get_climate_data(lat, lon)

    # Handle empty climate data
    if not climate_data or "trend_years" not in climate_data:
        climate_data = {
            "trend_years": list(range(1990, 2021)),
            "trend_values": [25 + (i * 0.1) for i in range(31)],
            "min_temps": [24 + (i * 0.1) for i in range(31)],
            "rainfall": [100 + i * 5 for i in range(31)],
            "coordinates": {"latitude": lat, "longitude": lon} if lat and lon else None
        }

    return render_template(
        "index.html",
        weather=weather_data,
        trend_years=climate_data["trend_years"],
        max_temps=climate_data["trend_values"],
        min_temps=climate_data["min_temps"],
        rainfall=climate_data["rainfall"],
        location=location,
        coordinates=climate_data.get("coordinates")
    )

@routes.route('/climate-news')
def climate_news():
    # Serve first page
    articles,next_page = get_climate_news()
    return render_template('climate-news.html', articles=articles,next_page=next_page)


@routes.route('/load-news')
def load_news():
    next_page = request.args.get('nextPage', type=int)
    articles, new_next_page = get_climate_news(next_page)

    html = render_template("news_fragment.html", articles=articles)
    return jsonify({
        "html": html,
        "next_page": new_next_page
    })

@routes.route('/climate-art')
def climate_art():
    posts= Post.query.order_by(Post.date_created.desc()).all()
    return render_template('climate-art.html', posts = posts)

@routes.route('/create', methods = ['GET','POST'])

def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title,content=content,author = current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post created")
        return redirect(url_for('main.index'))
    return render_template('create_post.html')



@routes.route('/climate-oracle')
@login_required
def climate_oracle():
    print("User is logged in:", current_user.username)
    return render_template('climate-oracle.html')



#ALL LOGIN LOGIC
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Login attempt - Username: {username}, Password: {password}")

        user = User.query.filter_by(username=username).first()
        print(f"User found: {user}")

        if user and password is not None and check_password_hash(user.password, password):
            login_user(user)
            print(f"Logged in user: {user.username}")
            flash('Logged in successfully.', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('routes.climate_oracle'))
        else:
            print("Login failed")
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


from flask_login import logout_user

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('routes.login'))


@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken', 'warning')
            return redirect(url_for('routes.register'))

        # Create user
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('routes.climate_oracle'))

    return render_template('register.html')


#ROUTES FOR THE ORACLE

def oracle_response(user_message: str) -> str:
    if "climate change" in user_message.lower():
        return "Climate change refers to long-term shifts in temperatures and weather patterns."
    elif "renewable" in user_message.lower():
        return "Renewable energy sources like solar and wind can greatly reduce emissions."
    else:
        return "I'm still learning . Could you ask about climate change, energy, or the environment?"

@routes.route("/oracle/chat", methods=["POST"])
def oracle_chat():
    data = request.get_json()
    user_message = data.get("message", "")
    response_text = oracle_response(user_message)
    return jsonify({"reply": response_text})


