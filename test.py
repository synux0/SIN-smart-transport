def get_distance(graph, origin_city, destination_city):    
    distances = {node: float('inf') for node in graph}
    distances[origin_city] = 0

    unvisited = set(graph.keys())

    while unvisited:
        current_city = min(unvisited, key=lambda node: distances[node])

        unvisited.remove(current_city)

        for neighbor in graph[current_city]:
            distance = distances[current_city] + 1

            if distance < distances[neighbor]:
                distances[neighbor] = distance

    return distances[destination_city]

def get_shortest_route(graph, origin_city, destination_city):
    distances = {node: float('inf') for node in graph}
    distances[origin_city] = 0
    previous_nodes = {node: None for node in graph}

    unvisited = set(graph.keys())

    while unvisited:
        current_city = min(unvisited, key=lambda node: distances[node])

        if current_city == destination_city:
            path = []
            while current_city is not None:
                path.append(current_city)
                current_city = previous_nodes[current_city]
            return list(reversed(path))

        unvisited.remove(current_city)

        for neighbor in graph[current_city]:
            distance = distances[current_city] + 1

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_city

    return None

graph = {
    'C0': {'a'},
    'C1': {'C0', 'C2'},
    'C2': {'C0', 'C1'}
}
#graph['C0'].add('hola')
emptyset = set('a')
graph['C0'] = emptyset
print(graph)