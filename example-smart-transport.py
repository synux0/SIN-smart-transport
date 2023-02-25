import pyhop


# Constant values

BUS_TICKET = 1.5


# Auxiliary functions

def taxi_rate(dist):
    return 1.5 + 0.5 * dist


# Operators: They return the state (if conditions are met) or False (if conditions are not met)
# Important: Operators CAN NOT be split up

def walk(state, a, x, y):
    if state.loc[a] == x:
        state.loc[a] = y
        return state
    else:
        return False


def call_taxi(state, a, x):
    if state.wants_taxi[a]:
        state.phoned_times[a] += 1
        state.loc['taxi'] = x
        return state
    else:
        return False


def wait_taxi(state, a):
    state.waiting_time[a] += 10
    return state


def read_book(state, a):
    state.read_book[a] = True
    return state


def ride_taxi(state, a, x, y):
    if state.loc['taxi'] == x and state.loc[a] == x:
        state.loc['taxi'] = y
        state.loc[a] = y
        state.owe[a] = taxi_rate(state.dist[x][y])
        return state
    else:
        return False


def pay_driver(state, a):
    if state.cash[a] >= state.owe[a]:
        state.cash[a] = state.cash[a] - state.owe[a]
        state.owe[a] = 0
        return state
    else:
        return False


# Declaration of operators. IT IS NOT ENOUGH to define them using "def",
# they also have to be specified to pyhop using "declare_operators".
# Important: ALL operators must be declared in a SINGLE "declare_operators" call.

pyhop.declare_operators(walk, call_taxi, wait_taxi, read_book, ride_taxi, pay_driver)
print()
pyhop.print_operators()


def move_the_truck_method(state, truck, city):
    

    return [('move_the_truck_op', truck, truck_next_position), ('move_the_truck_to_city', truck, city)]


def the_truck_already_in_city(state, truck, city):
    if state.trucks[truck]['location'] == city:
        return []
    
    return False

pyhop.declare_methods('move_the_truck_to_city', move_the_truck_method, the_truck_already_in_city)


def move_a_truck_method(state, city):
    # Search for a truck in city
    for truck in state.trucks.keys():
        if truck['location'] == city:
            return False
    
    # If no truck is present in city,
    # get the closest one and move it to city
    truck_to_move = find_closest_truck_to_city(city)

    return [('move_the_truck_to_city', truck_to_move, city)]


def a_truck_already_in_city(state, city):
    # Search for a truck in city
    for truck in state.trucks.keys():
        if truck['location'] == city:
            return []
    
    #If there was no truck found in city
    return False


pyhop.declare_methods('move_a_truck_to_city', move_a_truck_method, a_truck_already_in_city)


def deliver_package_method(state, goal, package):
    package_current_location = state.packages[package]['location']
    package_goal_location = goal.packages[package]['location']

    if package_current_location != package_goal_location:
        return [('move_a_truck_to_city', package_current_location), ('move_a_driver_to_city', package_current_location), ('deliver_package_to_city', goal, package)]
    
    return False


def package_already_delivered(state, goal, package):
    package_current_location = state.packages[package]['location']
    package_goal_location = goal.packages[package]['location']

    if package_current_location == package_goal_location:
        return []
    
    return False


pyhop.declare_methods('deliver_package', deliver_package_method, package_already_delivered)


def smart_transport_method(state, goal):
    for package in goal.packages.keys():
        package_current_location = state.packages[package]['location']
        package_goal_location = goal.packages[package]['location']

        if package_current_location != package_goal_location:
            return [('deliver_package', goal, package), ('smart_transport', goal)]
    
    for truck in goal.trucks.keys():
        truck_current_location = state.trucks[truck]['location']
        truck_goal_location = goal.trucks[truck]['location']

        if truck_current_location != truck_goal_location:
            return [('transport_truck', truck, goal), ('smart_transport', goal)]
    
    for driver in goal.drivers.keys():
        driver_current_location = state.drivers[driver]['location']
        driver_goal_location = goal.drivers[driver]['location']

        if driver_current_location != driver_goal_location:
            return [('transport_driver', driver, goal), ('smart_transport', goal)]

    return []


# Indicamos cual es la descomposicion de "smart-transport"

pyhop.declare_methods('smart_transport', smart_transport_method)
print()
pyhop.print_methods()


# State definition

state1 = pyhop.State('state1')

state1.drivers = {
    'D1': {'location': 'P_01', 'expenses': 0},
    'D2': {'location': 'C1', 'expenses': 0}
}

state1.packages = {
    'P1': {'location': 'C0'},
    'P2': {'locations': 'C0'}
}
    
state1.trucks = {
    'T1': {'location': 'C1', 'driver': 'none', 'cargo': {}},
    'T2': {'location': 'C0', 'driver': 'none', 'cargo': {}}
}

state1.track_connections = {
    'C0': {'P_01': 1},
    'P_01': {'C0': 1, 'C1': 1},
    'C1': {'P_01': 1, 'P_12': 1},
    'P_12': {'C1': 1, 'C2': 1},
    'C2': {'P_12': 1}
}

state1.road_connections = {
    'C0': {'C1': 1, 'C2': 1},
    'C1': {'C0': 1, 'C2': 1},
    'C2': {'C0': 1, 'C1': 1}
}


# Goal definition

goal1 = pyhop.Goal('goal1')

goal1.drivers['D1']['location'] = 'C0'

goal1.packages['P1']['location'] = 'C1'
goal1.packages['P2']['location'] = 'C2'

goal1.trucks['T1']['location'] = 'C0'

print("""
****************************************************************************************
Call pyhop.pyhop(state1,[('smart_transport', goal1)]) with different verbosity levels
****************************************************************************************
""")


# We try to obtain a plan from an initial state "state1" that meets the goal "goal1"

pyhop.pyhop(state1, [('smart_transport', goal1)], verbose=3)
