# Name: Niko Bransfield
# OSU Email: bransfim@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap with Separate Chaining (Part I)
# Due Date: 2024-03-14
# Description: HashMap implementation using a dynamic array and
#              separate chaining using singly linked lists.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Puts the given key-value pair into the hash map. If the key
        already exists in the map, its old value is replaced.
        :param key: The key to put into the hash map
        :param value: The value to assign to the key
        """
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        hash_index = self._hash_function(key) % self._capacity
        bucket: LinkedList = self._buckets[hash_index]
        entry = bucket.contains(key)
        if entry is not None:
            entry.value = value
        else:
            bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table and rehashes all existing
        key-value pairs.
        :param new_capacity: The minimum new capacity of the table. Must be
            a positive integer.
        """
        if new_capacity < 1:
            return
        entries = self.get_keys_and_values()

        # Note: because of how _next_prime() is implemented, this block will
        # incorrectly determine that the next prime after 1 is 3. However, this
        # behavior seems to be intentional.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity

        self.clear()
        for i in range(entries.length()):
            key, value = entries[i]
            self.put(key, value)

    def table_load(self) -> float:
        """
        Returns the hash table's load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        num_empty_buckets = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                num_empty_buckets += 1
        return num_empty_buckets

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key, or None if the key
        does not exist in the hash map.
        :param key: The key to search for
        :return: The value associated with the key, or None if the key doesn't
            exist in the hash map.
        """
        hash_index = self._hash_function(key) % self._capacity
        bucket: LinkedList = self._buckets[hash_index]
        entry = bucket.contains(key)
        if entry is not None:
            return entry.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Determines whether a key is present in the hash map.
        :param key: The key to search for
        :return: True if the key exists in the hash map, otherwise False.
        """
        hash_index = self._hash_function(key) % self._capacity
        bucket: LinkedList = self._buckets[hash_index]
        return bucket.contains(key) is not None

    def remove(self, key: str) -> None:
        """
        Removes a key and its associated value from the hash map.
        :param key: The key to remove
        """
        hash_index = self._hash_function(key) % self._capacity
        bucket: LinkedList = self._buckets[hash_index]
        if bucket.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Retrieves all the key-value pairs from the hash map.
        :return: A dynamic array containing each key-value pair in the hash map
            as tuples and in no particular order.
        """
        entries = DynamicArray()
        for i in range(self._capacity):
            bucket: LinkedList = self._buckets[i]
            for entry in bucket:
                entries.append((entry.key, entry.value))
        return entries

    def clear(self) -> None:
        """
        Clears the contents of the hash map. Does not change the underlying
        hash table capacity.
        """
        new_buckets = DynamicArray()
        for _ in range(self._capacity):
            new_buckets.append(LinkedList())
        self._size = 0
        self._buckets = new_buckets


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds the most occurring value(s) in the given array.
    :param da: The array to check
    :return: a tuple of: a dynamic array containing the value(s) which appear
        the most in the input array, and an integer representing the number
        of times each appears.
    """
    map = HashMap()
    mode_elements = DynamicArray()
    mode_value = 0

    for i in range(da.length()):
        element = da[i]
        count = map.get(element)
        if count is None:
            count = 0
        count += 1
        map.put(element, count)
        mode_value = mode_value if count <= mode_value else count

    entries = map.get_keys_and_values()
    for i in range(entries.length()):
        key, value = entries[i]
        if value == mode_value:
            mode_elements.append(key)
    return mode_elements, mode_value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
                  m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
                  m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(),
              round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu",
         "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
