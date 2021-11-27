from typing import List, Tuple

from app.entities import Vacuum, Plateau
from app.exceptions import InvalidRequest
from app.values import CardinalPoint, Coordinates, Instruction


class VacuumController:

    def handle(self, request: str) -> str:
        lines = request.strip().splitlines()
        if (len(lines) < 3
                or (len(lines) - 1) % 2 != 0):
            raise InvalidRequest(request)

        pieces = lines[0].strip().split(' ', 1)
        plateau = Plateau(Coordinates(int(pieces[0]), int(pieces[1])))
        vacuums: List[Tuple[Vacuum, List[Instruction]]] = []

        for i, line in enumerate(lines[1:]):
            if i % 2 == 0:
                pieces = line.strip().split(' ', 2)
                vacuum = plateau.add_vacuum(
                    Coordinates(int(pieces[0]), int(pieces[1])),
                    CardinalPoint(pieces[2])
                )
            else:
                instructions = [Instruction(letter) for letter in line.strip()]
                vacuums.append((vacuum, instructions))

        for vacuum, instructions in vacuums:
            for instruction in instructions:
                vacuum.process(instruction)

        response = ''
        for vacuum, _ in vacuums:
            response += f'{vacuum.position.x} {vacuum.position.y} {vacuum.heading.value}\n'

        return response.strip()
