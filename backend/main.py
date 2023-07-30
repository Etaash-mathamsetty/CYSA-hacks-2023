from flask import Flask, jsonify, request
import os
import databasemgr
import imageclass
# __name__ == __main__
app = Flask(__name__)

fake_backend = True


@app.route("/", methods=["GET"])
def demo_test():
    return "<p>Hello Hacker [Don't hack pls :(]</p>"


@app.route("/api/detect/<string:username>", methods=["POST", "GET"])
def process_image(username):
    images = request.files.getlist("images")
    if len(images) == 0 and request.method == "POST":
            return jsonify(
                {"error": "404", "message": "Please provide images with api request!"}
            )

    if request.method == "POST":
        for image in images:
                amount_of_images = len(os.listdir("Images"))
                image.save(os.path.join("Images", f"{amount_of_images + 1}.jpg"))
                return ""
        

    elif request.method == "GET":
        
        """
         copy_response = {}
        amount_of_images = len(os.listdir("Images"))
        class_labels = get_detections(os.path.join("Images", f"{amount_of_images}.jpg")) # the os.path.json thingy just gets the image name from the  folder
        response = send(class_labels)

        for result in response['results']:
            idd = result['id']
            title = result['title']
            title = title.replace(" ", "-")
            idx = response['results'].index(result)
            response['results'][idx]["url"] = "https://spoonacular.com/recipes/"+title + f"-{idd}"

        response['detections'] = class_labels
        print(response)
        return jsonify(response)
        """

        # process image stored data
        return jsonify({"message": f"success for {username}", "detections": ["blahblah"]})


# medicines_using is part of this as well
@app.route("/api/database/medicines/<string:username>", methods=["GET"])
def get_medicines(username):
    # exmpale

    if fake_backend:
        return jsonify(
            {"medicines": f"Tylenol,{username}", "medicines_using": "Tylenol"}
        )

    return False


@app.route("/api/database/user/<string:username>", methods=["GET"])
def get_user(username):
    if fake_backend:
        return jsonify({"Name": username, "Age": "35", "Gender": "M"})

    return False


@app.route("/api/database/user/setuser/<string:username>", methods=["GET"])
def set_user(username):
    return jsonify({"Message": f"Success for {username}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5600, debug=True)
