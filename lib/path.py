import itertools
import json
import sys
import time
from heapq import heappush, heappop

import numpy as np


def get_path(map_info, graph, start_map_id, end_map_id, start_cell=None, end_cell=None):
    potential_start_nodes_ids = []
    potential_end_nodes_ids = []
    start_cell_set = False if start_cell is None else True
    end_cell_set = False if end_cell is None else True
    for key, node in graph.items():
        if node['map_id'] == start_map_id:
            tmp_start_cell = node['cell'] if start_cell_set is False else start_cell
            cells = fetch_map_id(map_info, node['map_id'])['cells']
            if can_walk_to_node(cells_2_map(cells), tmp_start_cell, node):
                potential_start_nodes_ids.append(key)
        if node['map_id'] == end_map_id:
            tmp_end_cell = node['cell'] if end_cell_set is False else end_cell
            cells = fetch_map_id(map_info, node['map_id'])['cells']
            if can_walk_to_node(cells_2_map(cells), tmp_end_cell, node):
                potential_end_nodes_ids.append(key)

    couples = list(itertools.product(potential_start_nodes_ids, potential_end_nodes_ids))
    best_path, length = None, sys.maxsize
    for couple in couples:
        path = get_path_nodes(graph, couple[0], couple[1])
        if path is not False and len(path) < length:
            best_path = path
            length = len(path)
    return best_path


def fetch_map_id(map_info, map_id):
    for map in map_info:
        if map['id'] == map_id:
            return map
    raise Exception(f"Map not found {map_id}")


def can_walk_to_node(map, cell, node):
    start_pos = cell_2_coord(cell)
    goal_pos = cell_2_coord(node['cell'])

    neighbors = [(1, 1), (-1, -1), (1, -1), (-1, 1), (1, 0), (0, 1), (-1, 0), (0, -1)]

    close_set = set()
    came_from = {}
    gscore = {start_pos: 0}
    fscore = {start_pos: (goal_pos[0] - start_pos[0]) ** 2 + (goal_pos[1] - start_pos[1]) ** 2}
    oheap = []

    heappush(oheap, (fscore[start_pos], start_pos))

    while oheap:

        current = heappop(oheap)[1]

        if current == goal_pos:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return True

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + (neighbor[0] - current[0]) ** 2 + (neighbor[1] - current[1]) ** 2
            if 0 <= neighbor[0] < map.shape[0]:
                if 0 <= neighbor[1] < map.shape[1]:
                    if map[neighbor[0]][neighbor[1]] in [-1, 1, 2]:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + (goal_pos[0] - neighbor[0]) ** 2 + (goal_pos[1] - neighbor[1]) ** 2
                heappush(oheap, (fscore[neighbor], neighbor))

    return False


def cell_2_coord(cell):
    return (14 - 1 - cell % 14 + int((cell // 14) / 2)), cell % 14 + int((cell // 14) / 2 + 0.5)


def coord_2_cell(x, y):
    for i in range(560):
        if (x, y) == cell_2_coord(i):
            return i
    raise Exception(f"No cell found for {x, y}")


def cells_2_map(cells):
    maps = np.array(cells)
    shape = maps.shape
    flattened = maps.flatten()
    new_base = np.zeros((14 * shape[1] // 14 + 20 * shape[0] // 40 - 1, 14 * shape[1] // 14 + 20 * shape[0] // 40))
    new_base[new_base == 0] = -1
    for i in range(len(flattened)):
        coord = i % shape[1] + int((i // shape[1]) / 2 + 0.5), (shape[1] - 1 - i % shape[1] + int((i // shape[1]) / 2))
        new_base[coord[1]][coord[0]] = flattened[i]
    return new_base[:]


def get_path_nodes(graph, start_node_id, end_node_id):
    close_set = set()
    came_from = {}
    gscore = {start_node_id: 0}
    fscore = {start_node_id: heuristic(graph[start_node_id], graph[end_node_id])}
    oheap = []

    heappush(oheap, (fscore[start_node_id], start_node_id))

    while oheap:

        current = heappop(oheap)[1]

        if current == end_node_id:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            path = []
            map_id = 0
            for node_id in data:
                if graph[node_id]['map_id'] != map_id:
                    path.append({'coord': graph[node_id]['coord'], 'map_id': graph[node_id]['map_id'], 'cell': graph[node_id]['cell'], 'direction': graph[node_id]['direction']})
                    map_id = graph[node_id]['map_id']

            path.append({'coord': graph[start_node_id]['coord'], 'map_id': graph[start_node_id]['map_id'], 'cell': graph[start_node_id]['cell'], 'direction': graph[start_node_id]['direction']})
            return list(reversed(path[1:]))

        close_set.add(current)
        neighbours = graph[current]['neighbours']
        for neighbour in neighbours:
            tentative_g_score = gscore[current] + heuristic(graph[current], graph[neighbour])

            if neighbour in close_set and tentative_g_score >= gscore.get(neighbour, 0):
                continue

            if tentative_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1] for i in oheap]:
                came_from[neighbour] = current
                gscore[neighbour] = tentative_g_score
                fscore[neighbour] = tentative_g_score + heuristic(graph[neighbour], graph[end_node_id])
                heappush(oheap, (fscore[neighbour], neighbour))

    return False


def heuristic(node1, node2):
    coords_1 = [int(coord) for coord in node1['coord'].split(';')]
    coords_2 = [int(coord) for coord in node2['coord'].split(';')]
    return dist(coords_1, coords_2)


def dist(coord_1, coord_2):
    return ((coord_2[0] - coord_1[0]) ** 2 + (coord_2[1] - coord_1[1]) ** 2) ** 0.5


if __name__ == '__main__':
    mapinfo = []

    for i in range(10):
        with open('../assets/map_info_{}.json'.format(i), 'r', encoding='utf8') as f:
            mapinfo += json.load(f)
    graph = {}
    for i in range(3):
        with open('../assets/pathfinder_graph_{}.json'.format(i), 'r', encoding='utf8') as f:
            graph.update(json.load(f))

    print('Starting')
    start = time.time()
    print(get_path(mapinfo, graph, 146471, 172229642))
    print(time.time() - start)
