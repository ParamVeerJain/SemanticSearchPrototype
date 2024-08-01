import os
from flask import Flask,request,jsonify,send_from_directory
from pydantic import BaseModel
import search
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
IMAGE_FOLDER='/images/'
class QueryRequest(BaseModel):
    query: str

@app.route("/text_search",methods=['POST'])
def text_search():
    data = request.get_json()
    query = data.get('query')
    results=search.textSearch(query)
    return jsonify(results)
@app.route("/image-search",methods=['POST'])
def image_search():
    data = request.get_json()
    query = data.get('imagePath')
    results=search.imageSearch(query)
    return jsonify(results)
@app.route("/images/{productID}",methods=['GET'])
def get_images(image_name: str):
    file_path = f"images/{image_name}.jpg"
    return send_from_directory(IMAGE_FOLDER, image_name)

