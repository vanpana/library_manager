'''

@author: radu
'''
from enum import Enum, unique

from algorithms.bubble_sort import BubbleSort
from algorithms.bubble_sort import BubbleSort2
from algorithms.comb_sort import CombSort
from algorithms.gnome_sort import GnomeSort
from algorithms.insertion_sort import InsertionSort, InsertionSortRec
from algorithms.merge_sort import MergeSort
from algorithms.quick_sort import QuickSort


@unique
class Algorithm(Enum):
    BUBBLE_SORT = BubbleSort
    BUBBLE_SORT2 = BubbleSort2
    INSERTION_SORT = InsertionSort
    INSERTION_SORT_REC = InsertionSortRec
    QUICK_SORT = QuickSort
    MERGE_SORT = MergeSort
    GNOME_SORT = GnomeSort
    COMB_SORT = CombSort
