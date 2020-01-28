import websockets
import asyncio
import shell
import networkx
import flask

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
        for iteration in phase_vector:
            msg = {
                "phase_vector": iteration,
                "nodes_coordinates": nodes_coordinates,
                "node_edges": node_edges
            }
            await websocket.send(str(msg))
            print("msg send")


start_server = websockets.serve(serve_websocket, "localhost", 1234)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


