from app.entities import Surface
from app.exceptions import InvalidRequest, InvalidVacuumPosition, NoFurtherInstructions
from app.values import CardinalPoint, Coordinates, Instruction


class VacuumController:

    def handle(self, request: str) -> str:
        lines = request.strip().splitlines()
        if (len(lines) < 3
                or (len(lines) - 1) % 2 != 0):
            raise InvalidRequest(request)

        pieces = lines[0].strip().split(' ', 1)
        surface = Surface(Coordinates(int(pieces[0]), int(pieces[1])))

        for i, line in enumerate(lines[1:]):
            if i % 2 == 0:
                pieces = line.strip().split(' ', 2)
                position = Coordinates(int(pieces[0]), int(pieces[1]))
                direction = CardinalPoint(pieces[2])
            else:
                instructions = [Instruction(letter) for letter in line.strip()]
                surface.add_vacuum(
                    position,
                    direction,
                    instructions
                )

        any_instruction_processed = True
        while any_instruction_processed:
            any_instruction_processed = False
            for vacuum in surface.vacuums:
                try:
                    vacuum.process_next_instruction()
                except (InvalidVacuumPosition, NoFurtherInstructions):
                    pass
                else:
                    any_instruction_processed = True

        response = (
            'FAILED\n'
            if any(vacuum.pending_instructions for vacuum in surface.vacuums)
            else 'DONE\n'
        )
        for vacuum in surface.vacuums:
            response += f'{vacuum.position.x} {vacuum.position.y} {vacuum.direction.value}\n'

        return response.strip()
