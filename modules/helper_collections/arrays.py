"""Represent low-level arrays."""
import ctypes
from typing import Any, Iterator, Union


# Implements the Array ADT using array capabilities of the ctypes module.
class Array:
    """Represent a c array."""
    # Create an array with size elements.
    def __init__(self, size: int):
        assert size > 0, "Array size must be > 0"
        self._size = size
        # Create the array structure using the ctypes module.
        PyArrayType = ctypes.py_object * size
        self._elements = PyArrayType()
        # Initialize each element.
        self.clear(None)

    # Return the size of the array.
    def __len__(self) -> int:
        return self._size

    # Get the contents of the index element.
    def __getitem__(self, index: int):
        assert 0 <= index < len(self), "Array subscript out of range"
        return self._elements[index]

    # Put the value in the array element at index position.
    def __setitem__(self, index: int, value: Any):
        assert 0 <= index < len(self), "Array subscript out of range"
        self._elements[index] = value

    # Clear the array by setting each element to the given value.
    def clear(self, value: Any):
        """Fill the array with value."""
        for i in range(len(self)):
            self._elements[i] = value

    # Returns the array's iterator for traversing the elements.
    def __iter__(self) -> Iterator:
        return _ArrayIterator(self._elements)

    def __repr__(self) -> str:
        return "[" + ", ".join((str(i) for i in self)) + "]"


# An iterator for the Array ADT.
class _ArrayIterator:
    """Iterator for the low-level array."""

    def __init__(self, the_array: Array):
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> Any:
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        else:
            raise StopIteration


# Implementation of the Array2D ADT using an array of arrays.
class Array2D:
    """Create a 2D Array"""
    # Creates a 2 -D array of size numRows x numCols.

    def __init__(self, num_rows: int, num_cols: int):
        # Create a 1 -D array to store an array reference for each row.
        self.rows = Array(num_rows)

        # Create the 1 -D arrays for each row of the 2 -D array.
        for i in range(num_rows):
            self.rows[i] = Array(num_cols)

    # Returns the number of rows in the 2 -D array.
    def num_rows(self):
        """Return the number of the rows."""
        return len(self.rows)

    # Returns the number of columns in the 2 -D array.
    def num_cols(self):
        """Return the number of the cols"""
        return len(self.rows[0])

    # Clears the array by setting every element to the given value.
    def clear(self, value: Any):
        """Set every element of the array to value."""
        for row in range(self.num_rows()):
            self.rows[row].clear(value)

    # Gets the contents of the element at position [i, j]
    def __getitem__(self, index_tuple: Union[tuple, list]) -> Any:
        assert len(index_tuple) == 2, "Invalid number of array subscripts."
        row = index_tuple[0]
        col = index_tuple[1]
        assert 0 <= row < self.num_rows() and 0 <= col < self.num_cols(), \
            "Array subscript out of range."
        array_1d = self.rows[row]
        return array_1d[col]

    # Sets the contents of the element at position [i,j] to value.
    def __setitem__(self, index_tuple: Union[tuple, list], value: Any):
        assert len(index_tuple) == 2, "Invalid number of array subscripts."
        row = index_tuple[0]
        col = index_tuple[1]
        assert 0 <= row < self.num_rows() and 0 <= col < self.num_cols(), \
            "Array subscript out of range."
        array_1d = self.rows[row]
        array_1d[col] = value

    def __repr__(self) -> str:
        return "[" + ",\n ".join((str(self.rows[row])
                                 for row in range(self.num_rows()))) + "]"

    def __iter__(self) -> Iterator:
        return _ArrayIterator(self.rows)


class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""

    def __init__(self):
        """Create an empty array."""
        self._n = 0                                 # count actual elements
        self._capacity = 1                          # default array capacity
        self._A = self._make_array(self._capacity)  # low-level array

    def __len__(self) -> int:
        """Return number of elements stored in the array."""
        return self._n

    def __getitem__(self, k: int) -> Any:
        """Return element at index k."""
        if not 0 <= k < self._n:
            raise IndexError('invalid index')
        return self._A[k]                           # retrieve from array

    def append(self, obj: Any):
        """Add object to end of the array."""
        if self._n == self._capacity:               # not enough room
            self._resize(2 * self._capacity)        # so double capacity
        self._A[self._n] = obj
        self._n += 1

    def _resize(self, c: int):                      # nonpublic utitity
        """Resize internal array to capacity c."""
        B = self._make_array(c)                     # new (bigger) array
        for k in range(self._n):                    # for each existing value
            B[k] = self._A[k]
        self._A = B                                 # use the bigger array
        self._capacity = c

    @staticmethod
    def _make_array(c: int):                        # nonpublic utitity
        """Return new array with capacity c."""
        return (c * ctypes.py_object)()             # see ctypes documentation

    def insert(self, k: int, value: Any):
        """Insert value at index k, shifting subsequent values rightward."""
        if not (0 <= k <= self._n):
            raise ValueError("invalid index")
        if self._n == self._capacity:               # not enough room
            self._resize(2 * self._capacity)        # so double capacity
        for j in range(self._n, k, -1):             # shift rightmost first
            self._A[j] = self._A[j - 1]
        self._A[k] = value                          # store newest element
        self._n += 1

    def remove(self, value: Any):
        """Remove first occurrence of value(or  raise ValueError)."""
        # note: we do not consider shrinking the dynamic array in this version
        for k in range(self._n):
            if self._A[k] == value:                # found a match!
                for j in range(k, self._n - 1):    # shift others to fill gap
                    self._A[j] = self._A[j + 1]
                self._A[self._n - 1] = None        # help garbage collection
                self._n -= 1                       # we have one less item

                return None                            # exit immediately
        raise ValueError("value not found")        # only reached if no match