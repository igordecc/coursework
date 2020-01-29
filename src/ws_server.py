import websockets
import asyncio
import shell
import networkx
import json


async def serve_websocket(websocket, path):
    request = await websocket.recv()
    """
    Evaluate the dynamic system, and store all data in python local variables. Returns this variables for a future uses.
    """
    if request == 'load':
        # calculate and get data back
        phase_vector,  config = shell.compute_system_ocl_for_server()

        Aij, community_list, the_graph = config['Aij'], config['community_list'], config['topology']

        # flat map of 2-dimensional phase_vector.
        phase_vector = [[float(j) for j in i] for i in phase_vector]
        nodes_coordinates = [list(node) for node in networkx.drawing.fruchterman_reingold_layout(the_graph).values()]
        node_edges = [list(edge) for edge in networkx.edges(the_graph)]
        metadata = {
            "type" : "metadata",
            "metadata" :{
                "community_list": community_list,
                "phase_vector": [phase_vector[0], ],
                "nodes_coordinates": nodes_coordinates,
                "node_edges": node_edges
            }
        }
        await websocket.send(json.dumps(metadata))

        for i, iteration in enumerate(phase_vector):
            msg = {
                "type": "iteration",
                "iteration_data":{
                    "phase_vector": [iteration, ],
                },
                "dynamic_states":{
                    "nodes_coordinates": nodes_coordinates,
                    "node_edges": node_edges
                }
            }
            await websocket.send(json.dumps(msg))

    print("ok")


start_server = websockets.serve(serve_websocket, "localhost", 1234)
asyncio.get_event_loop().run_until_complete(start_server)
print("started server")
asyncio.get_event_loop().run_forever()
print("closed server")


