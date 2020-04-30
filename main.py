from __future__ import annotations
import os.path
import sys
import interpreter
import json_convert


def execute(program_file: str, map_file: str, argv: str, output_file: str):
    if os.path.isfile(program_file) and os.path.isfile(map_file) and os.path.isfile(output_file):
        map_dict, robot = json_convert.convert(map_file)
        with open(program_file, 'r') as pr_f:
            program = pr_f.read()
        intr = interpreter.Interpreter()
        intr.interpret(program, map_dict, robot, robot_mode=True, argv=argv.split())
        with open(output_file, 'w') as o:
            o.write(intr.map)
            o.write('\n\n')
            o.write(intr.robot)
    else:
        sys.stderr.write('Invalid file names')


if __name__ == '__main__':
    sys.stdout.write('Program path: ')
    prog = input()
    sys.stdout.write('Data path: ')
    data = input()
    sys.stdout.write('Argv: ')
    argv = input()
    sys.stdout.write('Output path: ')
    out = input()
    execute(prog, data, argv, out)
