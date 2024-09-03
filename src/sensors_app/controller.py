from time import sleep
from flask import Flask, request, render_template
from pymongo import MongoClient, errors, collection
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
import os


app = Flask("__name__")

http_requests_count = Counter('sensors_http_requests_count', 'Total HTTP Requests', ['method', 'endpoint'])
request_duration_seconds = Histogram('sensors_request_duration_seconds', 'Request duration in seconds', ['method', 'endpoint'])
http_error_count = Counter('sensors_http_error_count', 'Total HTTP errors', ['method', 'endpoint', 'status_code'])
http_error_arguments_count = Counter('sensors_http_error_arguments_count', 'Total HTTP errors due to bad arguments passed', ['method', 'endpoint', 'status_code', 'type'])
active_requests = Gauge('sensors_active_requests', 'Active HTTP requests', ['method', 'endpoint'])


def get_collection(name: str) -> collection.Collection:
    return MongoClient(os.environ['MONGO_HOST_NAME'], int(os.environ['MONGO_HOST_PORT'])).get_database("sensors").get_collection(name)


@app.post("/sensor")
def create_sensor():
    http_requests_count.labels(method=request.method, endpoint=request.path).inc()
    active_requests.labels(method=request.method, endpoint=request.path).inc()

    with request_duration_seconds.labels(method=request.method, endpoint=request.path).time():
        sensor = request.get_json()
        
        coll = get_collection("sensor")
        active_requests.labels(method=request.method, endpoint=request.path).dec()
        
        try:
            coll.insert_one(sensor)
            payload = {"result": "success"}
            code = 201
        except errors.DuplicateKeyError:
            http_error_arguments_count.labels(method=request.method, endpoint=request.path, status_code=403, type='duplicate key').inc()
            payload = {"result": "fail", "message": "Duplicate key (_id)"}
            code = 409
        
        return payload, code


@app.post("/data") # data_type passed usign url ?data_type=x
def insert_data():
    http_requests_count.labels(method=request.method, endpoint=request.path).inc()
    active_requests.labels(method=request.method, endpoint=request.path).inc()

    with request_duration_seconds.labels(method=request.method, endpoint=request.path).time():
        # GET data_type from parameters ?data_type=x
        data_type = request.args["data_type"]
        data = request.get_json()
        
        print(f"[FLASK] data type: {data_type} - data: {data}")
        
        if data_type == "temp":
            coll = get_collection("temp_data")
        elif data_type == "press":
            coll = get_collection("press_data")
        else:
            http_error_arguments_count.labels(method=request.method, endpoint=request.path, status_code=403, type='wrong data type').inc()
            return {"result": "fail"}, 403

    active_requests.labels(method=request.method, endpoint=request.path).dec()
    
    try:
        coll.insert_one(data)
    except:
        return {"result": "fail"}, 400

    return {"result": "success"}, 201
    

@app.route("/page", methods = ["get", "post"])
def www():
    temp_list = [el for el in get_collection("temp_data").find()]
    press_list = [el for el in get_collection("press_data").find()]

    return render_template( "test.html", name="Unnamed User", 
                            temp_data=temp_list, 
                            press_data=press_list
                        )


# Define a route to expose the metrics
@app.route('/metrics')
def metrics():
    metrics_data = generate_latest(http_requests_count) + generate_latest(request_duration_seconds) + generate_latest(http_error_count) + generate_latest(http_error_arguments_count)
    return metrics_data, 200, {'Content-Type': CONTENT_TYPE_LATEST}


@app.route('/active')
def long_running():
    sleep(5)


@app.errorhandler(Exception)
def handle_exception(e):
    status_code = 500
    if hasattr(e, 'code'):
        status_code = e.code

    http_error_count.labels(method=request.method, endpoint=request.path, status_code=status_code).inc()
    return [str(x) for x in e.args], status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    