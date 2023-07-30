from flask import Flask, jsonify, request

# __name__ == __main__
app = Flask(__name__)

fake_backend = True

@app.route('/', methods=['GET'])
def demo_test():
    return "<p>Hello Hacker [Don't hack pls :(]</p>"

@app.route('/api/detect/<string:username>', methods=['POST'])
def process_image(username):
    images = request.files.getlist("images")
    if len(images) == 0:
        return jsonify({"error": "404", "message" : "Please provide images with api request!"})
    
    #process data
    return jsonify({"message": f"success for {username}"})

    
# medicines_using is part of this as well
@app.route('/api/database/medicines/<string:username>', methods=['GET'])
def get_medicines(username):

    #exmpale
    
    if fake_backend:
        return jsonify({"medicines" : f"Tylenol,{username}", "medicines_using" : "Tylenol"})

    return False

@app.route('/api/database/user/<string:username>', methods=['GET'])
def get_user(username):

    

    if fake_backend:
        return jsonify({"Name" : username, "Age" : "35", "Gender" : "M"})

    return False

@app.route("/api/database/user/setuser/<string:username>", methods=["GET"])
def set_user(username):

    

    return jsonify({"Message": f"Success for {username}"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
