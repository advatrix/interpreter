import json
import cell
import robot
import os.path


def convert(file: str) -> tuple:
    """
    Convert .json file to map and robot initial data tuple

    Raises:
        FileNotFoundError
    """
    if os.path.isfile(file):
        with open(file, "r") as f:
            data = json.load(f)
            map_json_data = data["map"]
            robot_json_data = data["robot"]
            print(data)
            print(map_json_data)
            print(robot_json_data)
            map_dict = map_from_json(map_json_data)
            return map_dict, robot_json_data  # no need to convert robot_json_data
    else:
        raise FileNotFoundError


def map_from_json(data: dict) -> dict:
    """

    Raises:
        ValueError
    """
    ret = dict()
    for strkey, value in data.items():
        key = int(strkey)
        print(key)
        print(value)
        ret[key] = dict()
        for strk, v in value.items():
            k = int(strk)
            cell_type = v['type']
            if cell_type == 'empty':
                ret[key][k] = cell.Cell(key, k, cell.Empty())
            elif cell_type == 'box':
                ret[key][k] = cell.Cell(key, k, cell.Box(int(v['weight'])))
            elif cell_type == 'wall':
                ret[key][k] = cell.Cell(key, k, cell.Wall())
            elif cell_type == 'exit':
                ret[key][k] = cell.Cell(key, k, cell.Exit())
            else:
                raise ValueError
    print(ret)
    return ret


if __name__ == '__main__':
    filename = 'map.json'
    convert(filename)