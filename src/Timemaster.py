import datetime
import time


class Timemaster:

    def calc_truck_time(self, distance):
        """
        This method takes a parameter (the distance that was traveled by the truck) and with the given
        miles per hour value accumulates how much time, down to the second, the truck needs to make the trip,
        converts it and returns a :mod:`datetime.timedelta` object.

        .. note::
            Time-complexity is O(1).

        :param float distance: The distance the truck drove on its route
        :returns: The time the truck took to finish its route
        :type: :mod:`datetime.timedelta`
        """
        fraction_of_hour_traveled = distance / 18
        secs = fraction_of_hour_traveled * 3600
        hours, mins = divmod(secs, 3600)
        minutes, seconds = divmod(mins, 60)
        mins_secs_traveled = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
        truck_stopwatch = self.time_converted_to_timedelta(mins_secs_traveled)

        return truck_stopwatch

    def time_converted_to_timedelta(self, time):
        """
        This is a converter method that takes an argument, converts and returns the argument value as
        hours, minutes and seconds :func:`datetime.timedelta` object.

        .. note::
            Time-complexity is O(1).

        :param string time: in the format :mod:`00:00:00` to signify :mod:`hrs:mins:sec`
        :rtype: :mod:`datetime.timedelta`
        """
        (hrs, min, sec) = time.split(':')
        return datetime.timedelta(hours=int(hrs), minutes=int(min), seconds=int(sec))

    def military_to_normal_time(self, time_string):
        """
        This method changes military time format to normal am/pm time format

        Example:

        >>> print (Timemaster.military_to_normal_time('13:00:00'))
        01:00:00 PM

        .. note::
            Time-complexity is O(1).

        :param string time_string: military time in the format :mod:`13:01:57`
        :rtype: string
        """
        time_obj = time.strptime(time_string, '%H:%M:%S')
        normal_time = time.strftime("%r, %T ", time_obj)
        normal_time = normal_time[:11]
        return normal_time
