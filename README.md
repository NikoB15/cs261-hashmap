# HashMap
Niko Bransfield
Oregon State University  
CS261 Portfolio Project  
Completed 2024-03-14

## Overview
Hash map implementations using **chaining** and **open addressing**.

## Chaining - Required Methods
- `put(self, key: str, value: object) -> None`
  - Updates the key/value pair in the hash map. Doubles the hash table's capacity if the load factor >= 0.5.
- `resize_table(self, new_capacity: int) -> None`
  - Changes the capacity of the underlying table. All existing key/value pairs must be put into the new table, meaning the hash table links must be rehashed.
- `table_load(self) -> float`
  - Returns the current hash table load factor.
- `empty_buckets(self) -> int`
  - Returns the number of empty buckets in the hash table.
- `get(self, key: str) -> object`
  - Returns the value associated with the given key, or `None` if they key doesn't exist.
- `contains_key(self, key: str) -> bool`
  - Returns `True` if the given key exists in the hash map; otherwise, returns `False`.
- `remove(self, key: str) -> None`
  - Removes the given key and its associated value from the hash map. Does nothing if the given key does not exist.
- `get_keys_and_values(self) -> DynamicArray`
  - Returns a `DynamicArray` where each index contains a tuple of a key/value pair stored in the hash map. 
- `clear(self) -> None`
  - Clears the contents of the hash map without changing the capacity.
- `find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]`
  - A standalone function outside the `HashMap` class.
  - Receives a dynamic array, which is not guaranteed to be sorted.
  - Returns a tuple containing, in this order, a dynamic array comprising the mode (most occurring) value(s) of the given array, and an integer representing the highest frequency of occurrence for the mode value(s).

## Open Addressing - Required Methods
- `put(self, key: str, value: object) -> None`
  - Updates the key/value pair in the hash map. Doubles the hash table's capacity if the load factor >= 0.5.
- `resize_table(self, new_capacity: int) -> None`
  - Changes the capacity of the underlying table. All existing key/value pairs must be put into the new table, meaning the hash table links must be rehashed.
- `table_load(self) -> float`
  - Returns the current hash table load factor.
- `empty_buckets(self) -> int`
  - Returns the number of empty buckets in the hash table.
- `get(self, key: str) -> object`
  - Returns the value associated with the given key, or `None` if they key doesn't exist.
- `contains_key(self, key: str) -> bool`
  - Returns `True` if the given key exists in the hash map; otherwise, returns `False`.
- `remove(self, key: str) -> None`
  - Removes the given key and its associated value from the hash map. Does nothing if the given key does not exist.
- `get_keys_and_values(self) -> DynamicArray`
  - Returns a `DynamicArray` where each index contains a tuple of a key/value pair stored in the hash map. 
- `clear(self) -> None`
  - Clears the contents of the hash map without changing the capacity.
- Iterator methods:
  - `__iter__()`
  - `__next__()`
