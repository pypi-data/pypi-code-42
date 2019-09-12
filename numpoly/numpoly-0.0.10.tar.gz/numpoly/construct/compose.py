"""Compose polynomial from array of arrays of polynomials."""
import numpy
import numpoly

from .clean import postprocess_attributes


def compose_polynomial_array(
        arrays,
        dtype=None,
):
    """Compose polynomial from array of arrays of polynomials."""
    arrays = numpy.array(arrays, dtype=object)
    shape = arrays.shape
    if not arrays.size:
        return numpoly.ndpoly(shape=(0,), dtype=dtype)

    arrays = arrays.flatten()

    indices = numpy.array([isinstance(array, numpoly.ndpoly)
                           for array in arrays])
    arrays[indices] = numpoly.align_indeterminants(*arrays[indices])
    indeterminants = arrays[indices][0] if numpy.any(indices) else "q"
    arrays = arrays.tolist()

    dtypes = []
    keys = {(0,)}
    for array in arrays:
        if isinstance(array, numpoly.ndpoly):
            dtypes.append(array.dtype)
            keys = keys.union([tuple(key) for key in array.exponents.tolist()])
        elif isinstance(array, (numpy.generic, numpy.ndarray)):
            dtypes.append(array.dtype)
        else:
            dtypes.append(type(array))

    if dtype is None:
        dtype = numpy.find_common_type(dtypes, [])
    length = max([len(key) for key in keys])

    collection = {}
    for idx, array in enumerate(arrays):
        if isinstance(array, numpoly.ndpoly):
            for key, value in zip(array.exponents, array.coefficients):
                key = tuple(key)+(0,)*(length-len(key))
                if key not in collection:
                    collection[key] = numpy.zeros(len(arrays), dtype=dtype)
                collection[key][idx] = value
        else:
            key = (0,)*length
            if key not in collection:
                collection[key] = numpy.zeros(len(arrays), dtype=dtype)
            collection[key][idx] = array

    exponents = sorted(collection)
    coefficients = numpy.array([collection[key] for key in exponents])
    coefficients = coefficients.reshape(-1, *shape)

    exponents, coefficients, indeterminants = postprocess_attributes(
        exponents, coefficients, indeterminants)
    return numpoly.ndpoly.from_attributes(
        exponents=exponents,
        coefficients=coefficients,
        indeterminants=indeterminants,
    )
