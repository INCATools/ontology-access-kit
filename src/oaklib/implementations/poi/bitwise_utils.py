from typing import List, Iterator, Iterable


BITMAP = int


def bitmap_from_list(positions: Iterable[POS]) -> BITMAP:
    """
    Convert a list of indices to a bitmap.

    :param positions:
    :return:
    """
    v = 0
    for p in positions:
        v |= 1 << p
    return v


def map_bitmap_to_ints(bm: BITMAP) -> Iterator[POS]:
    """
    Convert a bitmap to a list of indices.

    :param bm:
    :return:
    """
    return [i for i in range(bm.bit_length()) if bm & (1 << i)]


def bitmap_cardinality(bm) -> int:
    # https://stackoverflow.com/questions/407587/python-set-bits-count-popcount
    # switch this for 3.10
    return bin(bm).count("1")
