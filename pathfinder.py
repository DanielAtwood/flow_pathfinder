from pprint import pprint


class Grid(object):
    def __init__(self, grid):
        self.grid = grid
        self.ids = self.get_ids()
        self.neighbors = self.all_neighbors()

    def get_ids(self):
        ids = set()
        for r in self.grid:
            ids.update(r)
        ids.remove(0)
        return ids

    def get_neighbors(self, pos):
        neighbors = [
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] - 1)
        ]

        value = grid[pos[0]][pos[1]]

        valid_neighbors = []
        while neighbors:
            r, c = n = neighbors.pop()

            if r < 0 or r > (len(self.grid) - 1):
                continue
            if c < 0 or c > (len(self.grid[r]) - 1):
                continue

            end = True if grid[r][c] is value else False
            if grid[r][c] is not 0 and not end:
                continue
            valid_neighbors.append(n)
        return valid_neighbors

    def all_neighbors(self):
        choice_dict = {}
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                choice_dict[(r, c)] = self.get_neighbors((r, c))
        return choice_dict

    def validate_end(self, pos, choices):
        for n in self.get_neighbors(pos):
            if pos not in choices[n]:
                choices[n].append(pos)

    def generate_path(self, current_path, pos):
        path = [current_path[-1]]
        choices = self.all_neighbors()

        self.validate_end(pos[1], choices)
        for step in path:
            neighbors = choices[step]
            valid_neighbors = []

            while neighbors:
                n = neighbors.pop()
                if n not in path and n not in current_path:
                    valid_neighbors.append(n)

            if len(valid_neighbors) == 1:
                path.append(valid_neighbors[0])
            elif len(valid_neighbors) > 1:
                new_path = current_path[:-1] + path
                return [new_path + [n] for n in valid_neighbors]

        return [current_path[:-1] + path]

    def get_paths(self, id):
        pos = []
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == id:
                    pos.append((r, c))

        paths = self.generate_path([pos[0]], pos)
        for path in paths:
            if pos[1] in path:
                continue

            new_paths = self.generate_path(path, pos)

            if new_paths[0] != path:
                paths.extend(new_paths)

        valid_paths = []
        while paths:
            path = paths.pop()
            if pos[1] in path:
                valid_paths.append(path)

        return valid_paths

    def solve(self):
        paths = {}
        valid_paths = []
        for id in self.ids:
            paths[id] = self.get_paths(id)

        keys = set(paths.keys())

        check_list = []
        id, check_start = paths.copy().popitem()
        for p in check_start:
            check_list.append({id: p})

        for path in check_list:
            key_diff = keys.difference(set(path.keys()))
            if not key_diff:
                continue

            id = key_diff.pop()
            rest = set()
            for i in path:
                rest.update(set(path[i]))

            for p in paths[id]:
                if not rest.intersection(set(p)):
                    path[id] = p
                    check_list.append(path)

                    key_diff = keys.difference(set(path.keys()))
                    all_pos = set(self.neighbors)
                    path_pos = rest.union(set(p))

                    if not key_diff and path_pos == all_pos:
                        valid_paths.append(path)
        return valid_paths


grid = (
    [1, 2, 0, 2, 3],
    [0, 0, 0, 0, 0],
    [4, 0, 3, 5, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 4, 5]
)

# grid = (
#     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
#     [0, 0, 3, 0, 0, 4, 5, 6, 0, 0, 7, 0, 0, 0],
#     [0, 0, 0, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
#     [8, 0, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
#     [0, 0, 0, 10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#     [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 12, 0, 0, 11, 0, 7, 13, 0, 0, 0, 0],
#     [0, 0, 0, 0, 14, 0, 13, 0, 6, 0, 3, 0, 0, 0],
#     [0, 0, 8, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 14, 15, 0, 0, 0, 15]
# )

g = Grid(grid)
pprint(g.solve())
# for p in g.solve():
# print(p)
