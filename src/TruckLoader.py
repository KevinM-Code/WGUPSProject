import csv
from HashMap import HashMap

package_info_custom_dict = HashMap()

truck_1_driver_1 = []
truck_2_driver_2 = []
truck_3_driver_1 = []

error_codes = HashMap()

# Set error codes and messages here
error_codes.set(1, ['Delivery address given to WGUPS reported incorrect. Processing Package...', '10:20:00'])

with open('CSV/PackageData.csv') as packages_file:
    package_data = csv.reader(packages_file, delimiter=',')


    for row in package_data:
        package_ID = int(row[0])
        pkg_address = row[1]
        pkg_city = row[2]
        pkg_state = row[3]
        pkg_zip = row[4]
        pkg_deliv_deadline = row[5]
        pkg_weight = row[6]
        pkg_notes = row[7]
        pkg_departure = ''
        delivery_error_code = ''
        status = 'At Hub'
        address_index = ''
        delivery_time = ''
        pkg_info_list = [package_ID, pkg_address, pkg_city, pkg_state, pkg_zip, pkg_deliv_deadline,
                         pkg_weight, pkg_notes, pkg_departure, delivery_error_code, status, address_index, delivery_time]

        # if delayed till 9:05, quickly put it on truck 2 that is leaving right after #

        if 'Delayed' in pkg_notes:
            truck_2_driver_2.append(pkg_info_list)
        # packages that have to be on Truck 2 put on Truck 2 #
        elif 'truck 2' in pkg_notes:
            truck_2_driver_2.append(pkg_info_list)
        # correct the wrong address this is done at 10:20 #
        elif 'Wrong address' in pkg_notes:
            pkg_info_list[1] = '410 S State St'
            pkg_info_list[4] = '84111'
            truck_3_driver_1.append(pkg_info_list)
        # If the delivery deadline is not anytime during the day
        # then the package must be delivered with other packages
        # All the "Must" are early packages and are grouped together #
        elif pkg_deliv_deadline != 'EOD':
            if '' in pkg_notes or 'Must' in pkg_notes:
                truck_1_driver_1.append(pkg_info_list)
        if pkg_info_list not in truck_1_driver_1 and pkg_info_list not in truck_3_driver_1 and pkg_info_list not in truck_2_driver_2:
            # If left over after going through all the above,
            # level off trucks 2 and 3 with all the rest of the packages
            if len(truck_2_driver_2) < len(truck_3_driver_1):
                truck_2_driver_2.append(pkg_info_list)
            else:
                truck_3_driver_1.append(pkg_info_list)

        package_info_custom_dict.set(package_ID, pkg_info_list)

