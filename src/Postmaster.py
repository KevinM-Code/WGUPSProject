# Kevin Mock #000966209

from Router import Router
from TruckLoader import truck_1_driver_1
from TruckLoader import truck_3_driver_1
from TruckLoader import truck_2_driver_2
from DataImporter import location_names
from TruckLoader import package_info_custom_dict
from Timemaster import Timemaster
from Packer import Packer
import re


FIRST_DEPARTURE_TIME = '8:00:00'
SECOND_DEPARTURE_TIME = '9:15:00'
THIRD_DEPARTURE_TIME = '11:00:00'

package_count = 40

pack = Packer()

time_master = Timemaster()


def main():
    """
    This is the :mod:`void` :func:`main` method. This drives the entire application. Each truck and the contents of the truck
    are run through the application. This allows easy scaling for more trucks, just add a line a code with the required parameters.
    """
    pack = Packer()
    route = Router()

    STARTING_LOCATION = 0

    # First Truck    
    truck_one_driver_one_total_mileage = float(run_route(FIRST_DEPARTURE_TIME, pack, route, truck_1_driver_1, STARTING_LOCATION))

    # Second Truck
    truck_two_driver_two_total_mileage = float(run_route(SECOND_DEPARTURE_TIME, pack, route, truck_2_driver_2, STARTING_LOCATION))

    # First Truck Second Trip
    truck_three_driver_one_total_mileage = float(run_route(THIRD_DEPARTURE_TIME, pack, route, truck_3_driver_1, STARTING_LOCATION))

    total_time = float(truck_one_driver_one_total_mileage + truck_two_driver_two_total_mileage + truck_three_driver_one_total_mileage)

    user_selection = greeting_and_search_type(total_time)

    if user_selection == '0':
        print('Thank you for using our system, please use us again!')
        exit()
    elif user_selection == '1':
        get_status_of_all_packages_at_time()
    elif user_selection == '2':
        track_package_by_package_num()


def run_route(departure_time, pack, route, truck, starting_location):
    """
    This method calls all the appropriate methods in order to get mileage, time of delivery and best route.

    Methods used:

        * :func:`Packer.Packer.add_departure_timestamp_and_location_index_to_package_info`
        * :func:`Router.Router.get_best_route`
        * :func:`Packer.Packer.calc_mileage_time_and_update_master_package_list`

    :param departure_time: the military time of departure e.g. :mod:`08:00:00`
    :type departure_time: string
    :param pack: an instance of the class :class:`Packer`
    :param route: an instance of the class :class:`Router`
    :param list truck: all the information from each of the packages on the truck
    :param int starting_location: the index of the starting location
    :return: The truck total milage
    """

    truck_and_trip = pack.add_departure_timestamp_and_location_index_to_package_info(departure_time, truck,
                                                                                     location_names)
    best_route = route.get_best_route(starting_location, truck_and_trip)
    truck_total_mileage = pack.calc_mileage_time_and_update_master_package_list(best_route, package_info_custom_dict,
                                                                                starting_location)
    return truck_total_mileage

def greeting_and_search_type(total_mileage):
    """
    This method displays the total distance of all the routes, the user interface greeting and allows the user to select
    from 3 options:

    The selections are:

        * 0 -- To exit the system
        * 1 -- to view delivery status of all packages at a particular time
        * 2 -- to get the status of a particular package

    The user selection is validated and returned.

    .. note::
            Time-complexity is O(1).

    :param float total_mileage: The mileage added together for all the trucks
    :return: The user selection 1, 2, or 3 only
    :rtype: string
    """
    print('Thank you for using our WGUPS Service!!')
    print('All packages were delivered ontime in %0.2f miles\n' % total_mileage)
    print('Below type:')
    print('\t0 - to exit the system')
    print('\t1 - to view delivery status of all packages at a particular time')
    print('\t2 - to get the status of a particular package\n')

    user_selection = input('PLEASE TYPE SELECTION HERE -> ')

    user_selection = exit_or_input_validation(user_selection, "^[12]$", 'choose 0, 1, or 2', 'PLEASE TYPE SELECTION HERE -> ')

    return user_selection


def exit_or_input_validation(user_input, regular_exp, error_message, new_prompt):
    """
    This is a reusable method that validates the user input so there are not any errors or sql injection like user input
    into the software.

    .. note::
            Time-complexity is O(1).

    :param string user_input: The user entered text
    :param string regular_exp: The regular expression that validates the input
    :param string error_message: The custom message that is add to "Incorrect, please" ...
    :param string new_prompt: This can be the same prompt text as the first request for a selection
    :return: The validated input
    :rtype: string
    """
    regex = re.compile(regular_exp)
    any_match = regex.match(user_input)

    # Allow the user to keep trying till the exit or get it right #
    while any_match is None:
        if user_input == '0':
            print('Thank you for using our system!!')
            exit()

        err_msg = '* Incorrect, please %s *' % error_message
        frame = ''.join(str('*') for char in err_msg)

        print(frame)
        print(err_msg)
        print(frame)

        user_input = input(new_prompt)
        any_match = regex.match(user_input)


    return user_input


def get_status_of_all_packages_at_time():
    """
    This method gets the status of all packages at a particular time.

    The results displayed for each package:

        * package ID
        * full delivery address
        * package weight
        * delivery status

    .. note::
            Time-complexity is O(N). The number of packages

    :return: void
    """
    time_prompt = 'Please enter a time in HH:MM:SS military format e.g. 12:30 PM is 12:30:00 - or 0 to exit: '
    time_query = input(time_prompt)
    time_query = exit_or_input_validation(time_query, "^([01]\d|2[0-3]):?([0-5]\d):?([0-5]\d)$",
                                  'enter the time in format HH:MM:SS e.g. 09:00:30', time_prompt)

    # to compare time, time must be in timedelta #
    time_query = time_master.time_converted_to_timedelta(time_query)
    pack_count = 1
    for package in range(package_count):

        # get departure time from package info HashMap #
        departure_time = time_master.time_converted_to_timedelta(package_info_custom_dict.get(pack_count)[8])
        # get delivery time from package info HashMap #
        delivery_time = time_master.time_converted_to_timedelta(package_info_custom_dict.get(pack_count)[12])
        # info that needs to be reported #
        package_id = str(package_info_custom_dict.get(pack_count)[0])
        full_address = package_info_custom_dict.get(pack_count)[1] + ', ' + package_info_custom_dict.get(pack_count)[2] \
                       + ', ' + package_info_custom_dict.get(pack_count)[3] + ', ' + package_info_custom_dict.get(pack_count)[4]
        delivery_deadline = package_info_custom_dict.get(pack_count)[5]
        package_weight = package_info_custom_dict.get(pack_count)[6]
        delivery_status = package_info_custom_dict.get(pack_count)[10]
        report = 'Package Id = %s  |  Address = %s  |  Delivery deadline = %s  |  Package weight = %s  |  Delivery status = %s'

        # time query is before departure -> At the Hub #
        if time_query <= departure_time:
            print(report % (package_id, full_address, delivery_deadline, package_weight, delivery_status))

        # time query is after departure and before delivery -> En Route #
        elif departure_time <= time_query <= delivery_time:
            delivery_status = 'In Route'
            print(report % (package_id, full_address, delivery_deadline, package_weight, delivery_status))
        # time query is after delivery -> Delivered
        elif time_query >= delivery_time:
            delivery_status = 'Delivered at ' + str(time_master.military_to_normal_time(package_info_custom_dict.get(pack_count)[12]))
            print(report % (package_id, full_address, delivery_deadline, package_weight, delivery_status))

        pack_count += 1


def track_package_by_package_num():
    """
    This method ask the user for the package number (can also be referred to as the tracking number) and then asks at
    what time during the day they would like to know where the package is. Once the user enters the information
    the results is displayed.

    The results displayed:

        * package ID
        * full delivery address
        * package weight
        * delivery status

    :return: void
    """
    id_prompt = 'Please enter the package ID number (also known as tracking number) - or 0 to exit: '
    id_query = input(id_prompt)
    id_query = exit_or_input_validation(id_query, "^([1-9]|[12]\d|3[0-9]|4[0])$", 'enter number of the package 1-40 e.g 12', id_prompt)

    time_prompt = 'Please enter a time in HH:MM:SS military format e.g. 12:30 PM is 12:30:00 - or 0 to exit: '
    time_query = input(time_prompt)
    time_query = exit_or_input_validation(time_query, "^([01]\d|2[0-3]):?([0-5]\d):?([0-5]\d)$",
                                          'enter the time in format HH:MM:SS e.g. 09:00:30', time_prompt)

    # get departure time from package info HashMap #
    departure_time = time_master.time_converted_to_timedelta(package_info_custom_dict.get(int(id_query))[8])
    # get delivery time from package info HashMap #
    delivery_time = time_master.time_converted_to_timedelta(package_info_custom_dict.get(int(id_query))[12])

    # info that needs to be reported #
    package_id = str(package_info_custom_dict.get(int(id_query))[0])
    full_address = package_info_custom_dict.get(int(id_query))[1] + ', ' + package_info_custom_dict.get(int(id_query))[2] \
                   + ', ' + package_info_custom_dict.get(int(id_query))[3] + ', ' + \
                   package_info_custom_dict.get(int(id_query))[4]
    delivery_deadline = package_info_custom_dict.get(int(id_query))[5]
    package_weight = package_info_custom_dict.get(int(id_query))[6]
    delivery_status = package_info_custom_dict.get(int(id_query))[10]
    report = 'Package Id = %s  |  Address = %s  |  Delivery deadline = %s  |  Package weight = %s  |  Delivery status = %s'

    # time query is before departure -> At the Hub #
    if time_master.time_converted_to_timedelta(time_query) <= departure_time:
        print(report % (package_id, full_address, delivery_deadline, package_weight, delivery_status))
    # time query is after departure and before delivery -> En Route #
    elif departure_time <= time_master.time_converted_to_timedelta(time_query) <= delivery_time:
        delivery_status = 'In Route'
        print(report % (package_id, full_address, delivery_deadline, package_weight, delivery_status))
    # time query is after delivery -> Delivered
    # Early deliveries have message that they are on time #
    elif time_master.time_converted_to_timedelta(time_query) >= delivery_time:
        delivery_status = 'Delivered at ' + str(time_master.military_to_normal_time(package_info_custom_dict.get(int(id_query))[12]))
        print(report % (package_id, full_address, delivery_deadline, package_weight, delivery_status))


if __name__ == "__main__":
    main()
