from flask import Flask, render_template,Blueprint,jsonify,request
from .api_utils import get_climate_data, get_climate_news,get_weather_data,get_coordinates


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


@routes.route('/climate-oracle')
def climate_oracle():
    return render_template('climate-oracle.html')

@routes.route('/climate-art')
def climate_art():
    return render_template('climate-art.html')
