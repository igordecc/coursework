import flask
import shell
import numpy
app = flask.Flask(__name__)

# adding answer to root '/'
@app.route('/')
def return_json_data():
    # calculate and get data back
    phase_vector, Aij, community_list = shell.compute_system_ocl_for_server()

    # TODO: check is this important or not
    phase_vector = [[float(j) for j in i] for i in phase_vector]

    # forming response
    response = flask.jsonify({"Aij": Aij.tolist(),"phase_vector": phase_vector, "community_list": community_list})
    response.headers.add('Access-Control-Allow-Origin', "*")    # security unimportant thing
    return response

if __name__== '__main__':
    app.run()