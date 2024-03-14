from flask import Flask, jsonify, request
from scraper import WebDriverManager 


app = Flask(__name__)


@app.route('/', methods=['POST'])
def scrape_youtube_videos():
    # Parse JSON data from request body
    request_data = request.json

    # Extract channel_name and n_videos from JSON data
    channel_name = request_data.get('channel_name')
    n_videos = request_data.get('n_videos')

    # Validate input parameters
    if not channel_name or not n_videos:
        return jsonify({"error": "Both 'channel_name' and 'n_videos' parameters are required."}), 400
    
    try:
        n_videos = int(n_videos)
    except ValueError:
        return jsonify({"error": "'n_videos' parameter must be an integer."}), 400

    # Initialize WebDriverManager and get video info
    try:
        webdriver_manager = WebDriverManager()
        scraped_video_info = webdriver_manager.get_video_info(channel_name, n_videos)
        return jsonify(scraped_video_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
