from DataImporter import distance_data


class Router:

    def total_mileage(self, row, col, total_dist):
        """
        This method refers to the :mod:`list` that was created from the file :download:`WGUPSDistances.csv <../../../src/CSV/WGUPSDistances.csv>`.
        Only the lower left triangle is filled in so the method tries to find a value by row and column, if no value is found it
        swaps the row and column values to find the distance between two locations. The method then adds the value looked up, to the :mod:`total_dist` value coming in as a parameter.

        .. note::
            This method has a time-complexity of O(1)

        :param int row: The row number
        :param int col: The column number
        :param float total_dist: This gives the method a looping accumulating capability (the distance is returned and can come right back in)
        :return: the mileage between the queried locations plus whatever has already been added.
        :rtype: float
        """
        if distance_data[row][col] == '' or distance_data[row][col] is None:
            dist = distance_data[col][row]
            total_dist += float(dist)
            return total_dist
        else:
            dist = distance_data[row][col]
            total_dist += float(dist)
            return total_dist


    def find_mileage(self, row, col):
        """
        This method refers to the :mod:`list` that was created from the file :download:`WGUPSDistances.csv <../../../src/CSV/WGUPSDistances.csv>`.
        Only the lower left triangle is filled in so the method tries to find a value by row and column, if no value is found it
        swaps the row and column values to find the distance between two locations.

        .. note::
            This method has a time-complexity of O(1)

        :param int row:
        :param int col:
        :return: The distance between deliveries
        :rtype: float
        """
        if distance_data[row][col] == '' or distance_data[row][col] is None:
            dist = distance_data[col][row]
            return float(dist)
        else:
            dist = distance_data[row][col]
            return float(dist)


    def get_best_route(self, location, packages_info_onboard):
        """
        Here is the workhorse of the application. It takes the starting point :mod:`location` and an array of packages
        on board :mod:`packages_info_onboard`. For every location, it finds the shortest route to the next location
        and continues till the end of the route, attempting to reorder the packages to a shorter route. The method then returns
        the packages and locations in the most efficient order a greedy algorithm can produce.

        .. note::
            This method has a time-complexity of O(N^2)

        :param int location: starting location
        :param list packages_info_onboard: an array of packages on board
        :return:
        """
        best_truck_route = []

        while len(packages_info_onboard) != 0:
            # start with a large number #
            best_move = 50
            # comment #
            iteration_num = 0
            # the index of the best move in the list of packages #
            index_of_best_move = 0
            # compare each of the locations in the route (that are left over) 
            # and find the shortest next location #
            for package in packages_info_onboard:
                # get the next potential route #
                package_destination_index = int(package[11])
                potential_route = self.find_mileage(int(location), int(package_destination_index))
                # if the next potential route is better than the current best 
                # so far move to that location for delivery  #
                if potential_route <= best_move:
                    best_move = potential_route
                    index_of_best_move = iteration_num
                iteration_num += 1

            # place the location on the end of the list #
            best_truck_route.append(packages_info_onboard[index_of_best_move])

            # go to the best location found #
            location = packages_info_onboard[index_of_best_move][11]
            # pop the location out of the list of locations cause it has been visited #
            packages_info_onboard.pop(index_of_best_move)

        return best_truck_route
