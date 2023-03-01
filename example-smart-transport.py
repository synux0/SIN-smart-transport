import pyhop


# Constant values

BUS_TICKET = 1.5


# Auxiliary functions


# Operators: They return the state (if conditions are met) or False (if conditions are not met)
# Important: Operators CAN NOT be split up

def move_the_driver_op(state, driver, next_city):
    current_city = state.drivers[driver]['location']

    if next_city in state.track_connections[current_city].keys():
        state.drivers[driver]['location'] = next_city
        return state
    else:
        return False


def move_the_truck_op(state, truck, next_city):
    current_city = state.trucks[truck]['location']

    if next_city in state.road_connections[current_city].keys():
        state.trucks[truck]['location'] = next_city
        return state
    else:
        return False

def load_package_op(state, package, truck):
    package_location = state.packages[package]['location']
    truck_location = state.trucks[truck]['location']

    if package_location == truck_location:
        state.packages[package]['location'] = truck
        state.trucks[truck]['cargo'].add(package)
        return state
    else:
        return False


def unload_package_op(state, package, truck):
    package_location = state.packages[package]['location']
    truck_location = state.trucks[truck]['location']

    if package_location == truck:
        state.packages[package]['location'] = truck_location
        state.trucks[truck]['cargo'].discard(package)
        return state
    else:
        return False


def load_driver_op(state, driver, truck):
    driver_location = state.drivers[driver]['location']
    truck_location = state.trucks[truck]['location']

    if driver_location == truck_location:
        state.drivers[driver]['location'] = truck
        state.trucks[truck]['driver'] = driver
        return state
    else:
        return False


def unload_driver_op(state, driver, truck):
    driver_location = state.drivers[driver]['location']
    truck_location = state.trucks[truck]['location']

    if driver_location == truck:
        state.drivers[driver]['location'] = truck_location
        state.trucks[truck]['driver'] = "none"
        return state
    else:
        return False


def pay_bus_ticket_op(state, driver):
    state.drivers[driver]['expenses'] += BUS_TICKET
    
    return state


# Declaration of operators. IT IS NOT ENOUGH to define them using "def",
# they also have to be specified to pyhop using "declare_operators".
# Important: ALL operators must be declared in a SINGLE "declare_operators" call.

pyhop.declare_operators(move_the_driver_op, move_the_truck_op, load_package_op, unload_package_op, load_driver_op, unload_driver_op, pay_bus_ticket_op)
print()
pyhop.print_operators()


def move_the_driver_method(state, driver, destination_city):
    current_city = state.drivers[driver]['location']

    if current_city != destination_city:
        next_city = get_next_city_by_track(current_city, destination_city)

        return [('move_the_driver_op', driver, next_city), ('move_the_driver', driver, destination_city)]
    return False


def the_driver_already_in_city(state, driver, destination_city):
    current_city = state.drivers[driver]['location']
    
    if current_city == destination_city:
        return []
    return False


pyhop.declare_methods('move_the_driver', move_the_driver_method, the_driver_already_in_city)


def move_the_driver_by_foot(state, driver, destination_city):
    distance = get_distance(state.drivers[driver]['location'], destination_city)

    if distance < 2:
        return [('move_the_driver', driver, destination_city)]
    
    return False


def move_the_driver_by_bus(state, driver, destination_city):
    distance = get_distance(state.drivers[driver]['location'], destination_city)

    if distance >= 2:
        return [('pay_bus_ticket_op', driver), ('move_the_driver', driver, destination_city)]
    
    return False


pyhop.declare_methods('move_the_driver_to_city', move_the_driver_by_foot, move_the_driver_by_bus)


def move_a_driver_method(state, destination_city):
    # Search for a driver in city
    for driver in state.drivers.keys():
        if driver['location'] == destination_city:
            return False
    
    # If no driver is present in city,
    # get the closest one and move it to city
    driver_to_move = find_closest_driver_to_city(destination_city)

    return [('move_the_driver_to_city', driver_to_move, destination_city)]


def a_driver_already_in_city(state, destination_city):
    # Search for a driver in city
    for driver in state.drivers.keys():
        if driver['location'] == destination_city:
            return []
    
    #If there was no driver found in city
    return False


pyhop.declare_methods('move_a_driver_to_city', move_a_driver_method, a_driver_already_in_city)


def move_the_truck_method(state, truck, destination_city):
    current_city = state.trucks[truck]['location']

    if current_city != destination_city:
        next_city = get_next_city_by_road(current_city, destination_city)

        return [('move_the_truck_op', truck, next_city), ('move_the_truck_to_city', truck, destination_city)]
    return False


def the_truck_already_in_city(state, truck, destination_city):
    current_city = state.trucks[truck]['location']

    if current_city != destination_city:
        return []
    
    return False

pyhop.declare_methods('move_the_truck_to_city', move_the_truck_method, the_truck_already_in_city)


def move_a_truck_method(state, destination_city):
    # Search for a truck in city
    for truck in state.trucks.keys():
        if truck['location'] == destination_city:
            return False
    
    # If no truck is present in city,
    # get the closest one and move it to city
    truck_to_move = find_closest_truck_to_city(destination_city)

    return [('move_the_truck_to_city', truck_to_move, destination_city)]


def a_truck_already_in_city(state, destination_city):
    # Search for a truck in city
    for truck in state.trucks.keys():
        if truck['location'] == destination_city:
            return []
    
    #If there was no truck found in city
    return False


pyhop.declare_methods('move_a_truck_to_city', move_a_truck_method, a_truck_already_in_city)


def deliver_package_to_city_method(state, goal, package):
    origin_city = state.packages[package]['location']
    destination_city = goal.packages[package]['location']

    # Get a truck in the same city as the package
    deliver_truck = ""
    for truck in state.trucks.keys():
        if truck['location'] == origin_city:
            deliver_truck = truck
    
    # Get a driver in the same city as the package
    deliver_driver = ""
    for driver in state.drivers.keys():
        if driver['location'] == origin_city:
             deliver_driver = driver

    return [('load_package_op', package, deliver_truck), ('load_driver_op', deliver_driver, deliver_truck), ('move_the_truck_to_city', deliver_truck, destination_city), ('unload_driver_op', deliver_driver, deliver_truck), ('unload_package_op', package, deliver_truck)]


pyhop.declare_methods('deliver_package_to_city', deliver_package_to_city_method)


def deliver_package_method(state, goal, package):
    package_current_location = state.packages[package]['location']
    package_goal_location = goal.packages[package]['location']

    if package_current_location != package_goal_location:
        return [('move_a_driver_to_city', package_current_location), ('move_a_truck_to_city', package_current_location), ('deliver_package_to_city', goal, package)]
    
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
            return [('move_a_driver_to_city', truck_current_location), ('move_the_truck_to_city', truck, truck_goal_location), ('smart_transport', goal)]
    
    for driver in goal.drivers.keys():
        driver_current_location = state.drivers[driver]['location']
        driver_goal_location = goal.drivers[driver]['location']

        if driver_current_location != driver_goal_location:
            return [('move_the_driver_to_city', driver, driver_goal_location), ('smart_transport', goal)]

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
