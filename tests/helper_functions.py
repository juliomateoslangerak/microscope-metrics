import pytest


def filter_dict(expected, analyzed):
    """
    Recursively filter the analyzed dictionary to retain only the keys in expected.
    """
    if isinstance(expected, dict) and isinstance(analyzed, dict):
        return {
            key: filter_dict(expected[key], analyzed[key]) for key in expected if key in analyzed
        }
    return analyzed  # Base case: return value directly if not a dict


def remove_np_pd_data(dataset):
    if isinstance(dataset, dict):
        return {
            k: remove_np_pd_data(v)
            for k, v in dataset.items()
            if k not in ["table_data", "array_data"]
        }
    return dataset


def approx_compare(expected, analyzed, rel_tol=1e-3, abs_tol=1e-3, int_tolerance=0):
    """
    Recursively compare expected and analyzed dictionaries allowing approximate matches:
    - Uses `pytest.approx` for floating point numbers.
    - Allows approximate integer comparison within `int_tolerance`.
    - Supports nested dataclasses.
    """
    if isinstance(expected, dict) and isinstance(analyzed, dict):
        return all(
            approx_compare(expected[key], analyzed[key], rel_tol, abs_tol, int_tolerance)
            for key in expected
            if key in analyzed
        )

    if isinstance(expected, list) and isinstance(analyzed, list):
        return all(
            approx_compare(exp, ana, rel_tol, abs_tol, int_tolerance)
            for exp, ana in zip(expected, analyzed)
        )

    if isinstance(expected, float) and isinstance(analyzed, float):
        return analyzed == pytest.approx(expected, rel=rel_tol, abs=abs_tol)

    if isinstance(expected, int) and isinstance(analyzed, int):
        return abs(expected - analyzed) <= int_tolerance  # Allow integer tolerance

    if isinstance(expected, str) and isinstance(analyzed, str):
        return expected.lower() == analyzed.lower()  # Case-insensitive match

    return expected == analyzed  # Default exact match for other types

