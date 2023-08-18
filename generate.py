#!/usr/bin/env python

from draftsman.blueprintable import Blueprint, BlueprintBook
from draftsman.constants import Direction
from draftsman.entity import ConstantCombinator, DeciderCombinator, ArithmeticCombinator, ProgrammableSpeaker, Lamp, ElectricPole

origin = (0, 0)

CLOCK_SIGNAL = "signal-A"
RANGE_START_SIGNAL = "signal-B"
RANGE_END_SIGNAL = "signal-C"
PLAY_SIGNAL = "signal-D"

blueprint = Blueprint()
blueprint.label = "Song"
blueprint.description = "A blueprint for a song"
blueprint.version = (1, 0)

# Create a counter
constant = ConstantCombinator()
constant.tile_position = (0, 0)
constant.direction = Direction.EAST
constant.set_signal(0, "signal-A", 1)
constant.id = "constant"

blueprint.entities.append(constant)

# clock
clock = DeciderCombinator()
clock.id = "clock"
clock.tile_position = (2, 0)
clock.direction = Direction.EAST
clock.set_decider_conditions("signal-A", "<=", 650, "signal-A", True)

blueprint.entities.append(clock)
blueprint.add_circuit_connection("red", "constant", "clock")
blueprint.add_circuit_connection("red", "clock", "clock", 2, 1)

def offset_position(pos, dx, dy):
    return (pos[0] + dx, pos[1] + dy)

def add_module(blueprint: Blueprint, delay, duration, note, position: (int, int)):
    namespace = "noteplayer_" + str(position[1]) + "_"

    pole = ElectricPole()
    pole.id = namespace + "pole"
    pole.position = position

    start_decider = DeciderCombinator()
    start_decider.id = namespace + "start"
    start_decider.direction = Direction.EAST
    start_decider.tile_position = offset_position(pole.position, 1, 0)
    start_decider.set_decider_conditions(CLOCK_SIGNAL, ">", delay, RANGE_START_SIGNAL, False)
    
    end_decider = DeciderCombinator()
    end_decider.id = namespace + "end"
    end_decider.direction = Direction.EAST
    end_decider.tile_position = offset_position(start_decider.tile_position, 2, 0)
    end_decider.set_decider_conditions(CLOCK_SIGNAL, "<=", delay + duration, RANGE_END_SIGNAL, False)

    play_decider = ArithmeticCombinator()
    play_decider.id = namespace + "play"
    play_decider.direction = Direction.EAST
    play_decider.tile_position = offset_position(end_decider.tile_position, 2, 0)
    play_decider.set_arithmetic_conditions(RANGE_START_SIGNAL, "AND", RANGE_END_SIGNAL, PLAY_SIGNAL)

    speaker = ProgrammableSpeaker()
    speaker.id = namespace + "speaker"
    speaker.tile_position = offset_position(play_decider.tile_position, 2, 0)
    speaker.allow_polyphony = False
    speaker.global_playback = True # there is no escape
    speaker.set_circuit_condition(PLAY_SIGNAL, ">", 0)
    speaker.instrument_name = "piano"
    speaker.note_name = note

    lamp = Lamp() # doona light tha candle! it'll bring the ghost!
    lamp.id = namespace + "lamp"
    lamp.set_circuit_condition(PLAY_SIGNAL, ">", 0)
    lamp.position = offset_position(speaker.tile_position, 1, 0)

    blueprint.entities.append(pole)
    blueprint.entities.append(start_decider)
    blueprint.entities.append(end_decider)
    blueprint.entities.append(play_decider)
    blueprint.entities.append(speaker)
    blueprint.entities.append(lamp)
    
    blueprint.add_circuit_connection("red", start_decider.id, end_decider.id, 1, 1)
    blueprint.add_circuit_connection("red", start_decider.id, end_decider.id, 2, 1)
    blueprint.add_circuit_connection("red", end_decider.id, play_decider.id, 1, 1)
    blueprint.add_circuit_connection("red", end_decider.id, play_decider.id, 2, 1)
    blueprint.add_circuit_connection("red", play_decider.id, speaker.id, 2, 1)
    blueprint.add_circuit_connection("red", speaker.id, lamp.id)

    blueprint.add_circuit_connection("green", pole.id, start_decider.id, 1, 1)
    blueprint.add_circuit_connection("green", pole.id, end_decider.id, 1, 1)

    if (position[1] == 2):
        blueprint.add_circuit_connection("green", "clock", pole.id, 2, 1)
    else:
        # connect to previous power pole
        last_pole = blueprint.find_entity_at_position(offset_position(pole.position, 0, -1))
        blueprint.add_circuit_connection("green", last_pole.id, pole.id)




add_module(blueprint, 0, 20, "C5", (2, 2))
add_module(blueprint, 20, 20, "D5", (2, 3))
add_module(blueprint, 60, 20, "C5", (2, 4))
add_module(blueprint, 80, 20, "E5", (2, 5))
add_module(blueprint, 120, 20, "E5", (2, 6))
add_module(blueprint, 160, 20, "D5", (2, 7))
add_module(blueprint, 200, 20, "C5", (2, 8))
add_module(blueprint, 240, 20, "D5", (2, 9))
add_module(blueprint, 300, 20, "G5", (2, 10))
add_module(blueprint, 320, 20, "G5", (2, 11))
add_module(blueprint, 360, 20, "D5", (2, 12))
add_module(blueprint, 380, 20, "E5", (2, 13))
add_module(blueprint, 420, 20, "D5", (2, 14))
add_module(blueprint, 440, 20, "F5", (2, 15))
add_module(blueprint, 480, 20, "F5", (2, 16))
add_module(blueprint, 520, 20, "G5", (2, 17))
add_module(blueprint, 540, 20, "A5", (2, 18))
add_module(blueprint, 580, 20, "G5", (2, 19))
blueprint_book = BlueprintBook()
blueprint_book.blueprints = [blueprint]
print(blueprint_book.to_string())