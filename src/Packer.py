
from DataImporter import first_7_letters_to_ascii_value
from Timemaster import Timemaster
from Router import Router

route = Router()
timer = Timemaster()

class Packer:
    
    def add_departure_timestamp_and_location_index_to_package_info(self, departure_time, truck, location_names):        
        """
        This method adds the departure time of the truck and using :func:`DataImporter.first_7_letters_to_ascii_value`
        then :mod:`DataImporter.location_names` instance of :class:`HashMap`, looks up and adds the index of the destination to each
        package information for faster lookup later.

        .. note::
            The time complexity is O(N)

        :param departure_time: The time of departure for the package that is on the truck
        :type departure_time: string constant
        :param list truck: The packages on the truck
        :param location_names: The destinations
        :type location_names: :class:`HashMap`
        :return: The updated list
        :rtype: list
        """
        x = 0
        packages = []
           
        for package in truck:
            # Insert the departure time
            truck[x][8] = departure_time
            # Get the ascii value from each of the first 7 characters, concatenate and use that as a key to lookup
            # the value in the location_names HashMap for the delivery location names array #
            location = location_names.get(int(first_7_letters_to_ascii_value(package[1])))
            # Out of that delivery location names array give the number of that location 
            # update the package info by adding the destination
            # index to the package on the truck #
            truck[x][11] = location[0]
            packages.append(truck[x])
            x += 1
        return packages

    def calc_mileage_time_and_update_master_package_list(self, best_route, package_info_custom_dict, starting_location):
        """
        This method totals up the mileage, keeps track of the time the truck takes to each stop and puts a timestamp of
        when the package was delivered to the master package list.

        .. note::
            The time complexity is O(N)

        :param list best_route: The best truck route produced from :func:`Router.Router.get_best_route`
        :param package_info_custom_dict: The master package list
        :type package_info_custom_dict: :class:`HashMap`
        :param starting_location: the index number of the location on the list of delivery places
        :type starting_location: int constant
        :return: The mileage the truck drove on the delivery route
        :rtype: float
        """
        package_delivery_order = 0
        truck_mileage_tally = 0
        iteration_num = 1

        for package in best_route:
            this_location = int(best_route[package_delivery_order][11])            
            if iteration_num == 1:
                # We are leaving from the hub on the first iteration #
                this_location = starting_location
                # To the first destination
                next_location = int(best_route[package_delivery_order][11])
            if len(best_route) != iteration_num and iteration_num > 1:
                # If it is not the last iteration get the location of the next delivery #
                next_location = int(best_route[package_delivery_order + 1][11])
            if len(best_route) == iteration_num and iteration_num > 1:
                # If it is the last iteration the next location is back to the Hub #
                next_location = starting_location
            # Through each iteration we lookup and tally the distance #    
            truck_mileage_tally = route.total_mileage(this_location, next_location, truck_mileage_tally)

            # Calculate how much time it takes from this location to the next and mark a lap time (like a stopwatch) after each iteration #
            delivery_stopwatch = timer.calc_truck_time(route.find_mileage(this_location, next_location))
            last_delivery_departure_time = best_route[package_delivery_order - 1][12]
            if (package_delivery_order == 0):
                last_delivery_departure_time = best_route[package_delivery_order][8]
            delivery_lap_time = timer.time_converted_to_timedelta(str(last_delivery_departure_time)) + timer.time_converted_to_timedelta(str(delivery_stopwatch))
            best_route[package_delivery_order][12] = str(delivery_lap_time)
            package_info_custom_dict.set(int(best_route[package_delivery_order][0]), best_route[package_delivery_order])
            package_delivery_order += 1
            iteration_num += 1

        return truck_mileage_tally

