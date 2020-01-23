import flask
import shell
import networkx
import numpy
app = flask.Flask(__name__)
print("ok")
# adding answer to root '/'
@app.route('/')
def return_json_data():
    # calculate and get data back
    phase_vector,  config = shell.compute_system_ocl_for_server()
    Aij, community_list, the_graph = config['Aij'], config['community_list'], config['topology']
    # TODO: check is this important or not
    phase_vector = [[float(j) for j in i] for i in phase_vector]
    nodes_coordinates = [list(node) for node in networkx.drawing.fruchterman_reingold_layout(the_graph).values()]
    node_edges = [list(edge) for edge in networkx.edges(the_graph)]
    # forming response
    response = flask.jsonify({"Aij": Aij.tolist(),
                              "phase_vector": phase_vector,
                              "community_list": community_list,
                              "nodes_coordinates":nodes_coordinates,
                              "node_edges":node_edges
                              })

    response.headers.add('Access-Control-Allow-Origin', "*")    # security unimportant thing
    return response

@app.route('/dynamic')
def return_dynamic_data():
    # return certain data to certain user
    # can it work?
    ...


if __name__== '__main__':
    app.run()