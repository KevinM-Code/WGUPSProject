# Kevin Mock

class HashMap:
    """
    This :class:`HashMap` has an insertion, deletion, and search time-complexity is O(N). However on average,
    time-complexity is a good Θ(1).
    """

    # Complexity is O(1)
    def __init__(self):
        self.starting_bucket_size = 17  # prime number of buckets
        self.hashmap = [[] for x in range(0, self.starting_bucket_size)]

    def _calc_hash(self, key):
        """
        This private method takes and int and returns what bag number it will be put into.

        .. note::
            Time-complexity is O(1).
        
        :param int key: The key value
        :return: bag number
        :rtype: int
        """
        
        bag_num = int(key) % self.starting_bucket_size
        return bag_num

    # Complexity is O(N)
    def set(self, key, value):
        """
        This method sets the key-value pair in the :class:`HashMap`.

        .. note::
            This method has a time-complexity of O(N)
           
        :param key: ID for the value
        :type key: int
        :param value: A :mod:`list` of information
        :type value: :mod:`list` or any
        """        
        hash_key = self._calc_hash(key)
        key_exists = False
        bag = self.hashmap[hash_key]
        for x, kv in enumerate(bag):
            curr_key, curr_val = kv
            if key == curr_key:
                key_exists = True
                break
        if key_exists:
            bag[x] = (key, value)
        else:
            bag.append((key, value))

    # Complexity is O(N)
    def get(self, key):
        """
        With the key given as a parameter, this method returns the value assigned to the key.

        .. note::
            This method has a time-complexity of O(N)

        :param int key: ID for the value
        :return: A :mod:`list` of information
        :rtype: :mod:`list` or any
        """
        hash_key = self._calc_hash(key)
        bag = self.hashmap[hash_key]
        position_in_bag = 0
        for kv in bag:

            curr_key, curr_val = kv
            if key == curr_key:
                #Caching the retrieve key-value
                bag.insert(0, bag.pop(position_in_bag))
                return curr_val
            position_in_bag += 1
        else:
            raise KeyError('The key does not exist.')

    # Complexity is O(N)
    def remove(self, key):
        """
        This method removes the key value pair from the :class:`HashMap` based on the key.

        .. note::
            Time-complexity is O(N)

        :param int key: ID for the value
        :return: A :mod:`list` of information
        :rtype: :mod:`list` or any
        """
        hash_key = self._calc_hash(key)
        if self.hashmap[hash_key] is None:
            return False
        for i in range(0, len(self.hashmap[hash_key])):
            if self.hashmap[hash_key][i][0] == key:
                self.hashmap[hash_key].pop(i)
                return True

