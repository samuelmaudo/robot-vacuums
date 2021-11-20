from collections import OrderedDict
from typing import Dict, List

from app.entities import Mower, Plateau
from app.exceptions import InvalidRequest
from app.values import CardinalPoint, Coordinates, Instruction


class MowerController:

    def handle(self, request: str) -> str:
        lines = request.strip().splitlines()
        if (len(lines) < 3
                or (len(lines) - 1) % 2 != 0):
            raise InvalidRequest(request)

        pieces = lines[0].strip().split(' ', 1)
        plateau = Plateau(Coordinates(int(pieces[0]), int(pieces[1])))
        mowers: Dict[Mower, List[Instruction]] = OrderedDict()

        for i, line in enumerate(lines[1:]):
            if i % 2 == 0:
                pieces = line.strip().split(' ', 2)
                mower = plateau.add_mower(
                    Coordinates(int(pieces[0]), int(pieces[1])),
                    CardinalPoint(pieces[2])
                )
            else:
                instructions = [Instruction(letter) for letter in line.strip()]
                mowers[mower] = instructions

        for mower, instructions in mowers.items():
            for instruction in instructions:
                mower.process(instruction)

        response = ''
        for mower in mowers.keys():
            response += f'{mower.position.x} {mower.position.y} {mower.heading.value}\n'

        return response.strip()
