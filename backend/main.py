import json
from flask import Flask, jsonify, request
import os
import databasemgr
import imageclass
import requests
import openai
from dotenv import load_dotenv
load_dotenv

openai.api_key = os.getenv("OPENAI_API_KEY")

# __name__ == __main__
app = Flask(__name__)
fake_backend = False


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
        
        amount_of_images = os.listdir("Images")
        detections = []
        for image in amount_of_images:
            class_labels = imageclass.get_classification(os.path.join("Images", image))
            os.remove(os.path.join("Images", image))
            for label in class_labels:
                if label not in detections:
                    detections.append(label)
        
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
        return jsonify({"message": f"success for {username}", "detections": detections})





@app.route("/api/database/user/<string:username>", methods=["GET"])
def get_user(username):
    if fake_backend:
        return jsonify({"Name": username, "Age": "35", "Gender": "M"})

    value = eval(databasemgr.read(username))
    return jsonify({"name": value['name'], "age": value['age'], "gender": value['gender']})


# @app.route("/api/database/user/init/<string:username>/<string:name>/<string:age>/<string:gender>", methods=["GET"])
# def set_user(username, name, age, gender):

#     dict = {'name': name, 'age': age, 'gender': gender}
#     databasemgr.write(username, str(dict))
#     return jsonify({"Message": f"Success for {username}"})
@app.route("/api/meds/del/<string:username>/<int:index>", methods=["GET"])
def delete_med_based_on_index(username, index):
    meds_info = eval(databasemgr.read(username))
    cur_meds = eval(meds_info['medicines'])
    cur_meds.pop(index)
    meds_info['medicines'] = cur_meds
    databasemgr.write(username, json.dumps(meds_info))
    return jsonify({"code": 200, "msg": "success"})


@app.route("/myhealthboxapi/search/<string:name>")
def serach_product(name):
    

    url = "https://myhealthbox.p.rapidapi.com/search/fulltext"

    querystring = {"q":name,"c":"us","l":"en","limit":"10","from":"0"}

    headers = {
	"X-RapidAPI-Key": f"{os.getenv('RAPID')}", #i'll give you it later
	"X-RapidAPI-Host": "myhealthbox.p.rapidapi.com"
    }


    response = requests.get(url, headers=headers, params=querystring)
    
    # print(response.json())

    if response.json()["total_results"] >= 1:


        firstResultID = response.json()["result"][0]["product_id"]
        one_product_info_url = "https://myhealthbox.p.rapidapi.com/product/info"
        querystring = {"product_id": firstResultID}
        response = requests.get(one_product_info_url, headers=headers, params=querystring)
        js = response.json()
        js["code"] = 200
        return jsonify(js)

    else:
        return jsonify({"code":"400", "msg":"search invalid - no results returned"})
    # print(response.json())

@app.route("/medsapi/infos/<string:username>", methods=["POST"])
def save_meds(username):
    if not os.path.exists("meds"):
        os.mkdir("meds")
    if not os.path.exists(f"meds/{username}"):
        os.mkdir(f"meds/{username}")
    
    content = request.json
    content = content['data']
    # content is in a list 
    # {"med1" : {},
    # "med2" : {}}

    meds_info = eval(databasemgr.read(username))
    cur_meds = eval(meds_info['medicines'])
    cur_meds.extend(content)
    meds_info['medicines'] = json.dumps(cur_meds)
    databasemgr.write(username, json.dumps(meds_info))

    return jsonify({"Message": f"Success for {username}"})

# medicines_using is part of this as well
@app.route("/api/database/medicines/<string:username>", methods=["GET"])
def get_medicines(username):
    # exmpale

    if fake_backend:
        return jsonify(
            {"medicines": f"Tylenol,{username}", "medicines_using": "Tylenol"}
        )

    value = eval(databasemgr.read(username))

    return jsonify({'medicines': value['medicines'], 'medicines_using': value['medicines_using']})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5600, debug=True)
