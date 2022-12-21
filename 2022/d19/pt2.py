import math
import re
from multiprocessing import Pool

SOURCE_FILE = 'numbers.txt'

MINUTES = 32
BUILD_TIME = 1

RESOURCE_ORE = 'ore'
RESOURCE_CLAY = 'clay'
RESOURCE_OBSIDIAN = 'obsidian'
RESOURCE_GEODE = 'geode'
RESOURCES = [RESOURCE_ORE, RESOURCE_CLAY, RESOURCE_OBSIDIAN, RESOURCE_GEODE]

ROBOT_ORE = 'robot_ore'
ROBOT_CLAY = 'robot_clay'
ROBOT_OBSIDIAN = 'robot_obsidian'
ROBOT_GEODE = 'robot_geode'
ROBOTS = [ROBOT_ORE, ROBOT_CLAY, ROBOT_OBSIDIAN, ROBOT_GEODE]

ROBOT_TO_ORE = {
  ROBOT_ORE: RESOURCE_ORE,
  ROBOT_CLAY: RESOURCE_CLAY,
  ROBOT_OBSIDIAN: RESOURCE_OBSIDIAN,
  ROBOT_GEODE: RESOURCE_GEODE,
}

blueprint = dict[str, dict[str, int]]


class State:
  def __init__(self, robots: dict[str, int], resources: dict[str, int], time: int):
    self.robots = robots
    self.resources = resources
    self.time = time

  def __str__(self):
    return f'State. robots: {self.robots} resources: {self.resources} time: {self.time}'

  def as_hash(self):
    return f'{self.robots}{self.resources}'


def find_max_geode(blueprint: blueprint):
  queue = [State({robot: 0 for robot in ROBOTS} | {ROBOT_ORE: 1}, {resource: 0 for resource in RESOURCES}, 0)]
  max_geodes = 0
  seen_states: dict[str, int] = {}

  while len(queue) > 0:
    current_state = queue.pop()
    if (current_state.as_hash() in seen_states and seen_states[current_state.as_hash()] <= current_state.time) \
        or (MINUTES - current_state.time + 4) * (MINUTES - current_state.time + 4) / 2 + \
        current_state.resources[RESOURCE_GEODE] < max_geodes:
      continue
    seen_states[current_state.as_hash()] = current_state.time
    # print(current_state, max_geodes)
    income_ores = {ROBOT_TO_ORE[robot]: amount for robot, amount in current_state.robots.items() if amount > 0}
    # print('income', income_ores)
    for robot_name in ROBOTS[::-1]:
      robot_build_resources = blueprint[robot_name]
      if set(robot_build_resources.keys()).issubset(income_ores.keys()) and (robot_name == ROBOT_GEODE or all(
          income_ores[resource] <= amount for resource, amount in robot_build_resources.items()
      )):
        # can build this robot
        mine_time = max(
          [math.ceil((amount - current_state.resources[robot_resource]) / income_ores[robot_resource])
           for robot_resource, amount in robot_build_resources.items()] + [0]
        )
        if current_state.time + mine_time < MINUTES:
          resources_consumed = {
            resource: robot_build_resources[resource] if resource in robot_build_resources.keys() else 0
            for resource in RESOURCES
          }
          # update state with robot built
          queue.append(State(
            current_state.robots | {robot_name: current_state.robots[robot_name] + 1},
            {
              ROBOT_TO_ORE[robot]: current_state.resources[ROBOT_TO_ORE[robot]] + count * (mine_time + BUILD_TIME) -
                                   resources_consumed[ROBOT_TO_ORE[robot]]
              for robot, count in current_state.robots.items()
            },
            current_state.time + mine_time + BUILD_TIME
          ))

      # use remaining time to mine
      if current_state.robots[ROBOT_GEODE] > 0:
        end_geodes = current_state.resources[RESOURCE_GEODE] + current_state.robots[ROBOT_GEODE] * \
                     (MINUTES - current_state.time)
        if end_geodes > max_geodes:
          max_geodes = end_geodes

  print('found max', max_geodes)
  return max_geodes


def run():
  robot_blueprints: list[blueprint] = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      bot_numbers = re.match(
        r'Blueprint .*: Each ore robot costs (.*) ore. Each clay robot costs (.*) ore. Each obsidian robot costs (.*) ore and (.*) clay. Each geode robot costs (.*) ore and (.*) obsidian.',
        line)
      robot_blueprints.append({
        ROBOT_ORE: {
          RESOURCE_ORE: int(bot_numbers.groups()[0])
        },
        ROBOT_CLAY: {
          RESOURCE_ORE: int(bot_numbers.groups()[1]),
        },
        ROBOT_OBSIDIAN: {
          RESOURCE_ORE: int(bot_numbers.groups()[2]),
          RESOURCE_CLAY: int(bot_numbers.groups()[3])
        },
        ROBOT_GEODE: {
          RESOURCE_ORE: int(bot_numbers.groups()[4]),
          RESOURCE_OBSIDIAN: int(bot_numbers.groups()[5]),
        }
      })

  robot_blueprints = robot_blueprints[:3]

  with Pool(3) as p:
    results = p.map(find_max_geode, robot_blueprints)
  print(math.prod(results))


if __name__ == '__main__':
  run()
