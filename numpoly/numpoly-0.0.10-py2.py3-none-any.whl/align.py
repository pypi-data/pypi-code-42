"""Align polynomials."""
import numpy
import numpoly


def align_polynomials(*polys):
    """
    Align polynomial such that dimensionality, shape, etc. are compatible.

    Args:
        polys (numpoly.ndpoly):
            Polynomial to make adjustment to.

    Returns:
        (Tuple[numpoly.ndpoly, ...]):
            Same as ``polys``, but internal adjustments made to make them
            compatible for further operations.

    """
    polys = align_shape(*polys)
    polys = align_indeterminants(*polys)
    polys = align_exponents(*polys)
    return polys


def align_shape(*polys):
    """
    Align polynomial by shape.

    Args:
        polys (numpoly.ndpoly):
            Polynomial to make adjustment to.

    Returns:
        (Tuple[numpoly.ndpoly, ...]):
            Same as ``polys``, but internal adjustments made to make them
            compatible for further operations.

    Examples:
        >>> x, y = numpoly.symbols("x y")
        >>> poly1 = 4*x
        >>> poly2 = numpoly.polynomial([[2*x+1, 3*x-y]])
        >>> print(poly1.shape)
        ()
        >>> print(poly2.shape)
        (1, 2)
        >>> poly1, poly2 = numpoly.align_shape(poly1, poly2)
        >>> print(poly1)
        [[4*x 4*x]]
        >>> print(poly2)
        [[1+2*x -y+3*x]]
        >>> print(poly1.shape)
        (1, 2)
        >>> print(poly2.shape)
        (1, 2)

    """
    polys = [numpoly.aspolynomial(poly) for poly in polys]
    common = 1
    for poly in polys:
        common = numpy.ones(poly.coefficients[0].shape, dtype=int)*common

    polys = [poly.from_attributes(
        exponents=poly.exponents,
        coefficients=[coeff*common for coeff in poly.coefficients],
        indeterminants=poly.indeterminants,
    ) for poly in polys]
    assert numpy.all(common.shape == poly.shape for poly in polys)
    return tuple(polys)


def align_indeterminants(*polys):
    """
    Align polynomial by indeterminants.

    Args:
        polys (numpoly.ndpoly):
            Polynomial to make adjustment to.

    Returns:
        (Tuple[numpoly.ndpoly, ...]):
            Same as ``polys``, but internal adjustments made to make them
            compatible for further operations.

    Examples:
        >>> x, y = numpoly.symbols("x y")
        >>> poly1, poly2 = numpoly.polynomial([2*x+1, 3*x-y])
        >>> print(poly1.indeterminants)
        [x]
        >>> print(poly2.indeterminants)
        [x y]
        >>> poly1, poly2 = numpoly.align_indeterminants(poly1, poly2)
        >>> print(poly1)
        1+2*x
        >>> print(poly2)
        -y+3*x
        >>> print(poly1.indeterminants)
        [x y]
        >>> print(poly2.indeterminants)
        [x y]

    """
    polys = [numpoly.aspolynomial(poly) for poly in polys]
    common_indeterminants = sorted({
        indeterminant
        for poly in polys
        if not poly.isconstant()
        for indeterminant in poly.names
    })
    if not common_indeterminants:
        return polys

    for idx, poly in enumerate(polys):
        indices = numpy.array([
            common_indeterminants.index(indeterminant)
            for indeterminant in poly.names
            if indeterminant in common_indeterminants
        ])
        exponents = numpy.zeros(
            (len(poly.keys), len(common_indeterminants)), dtype=int)
        if indices.size:
            exponents[:, indices] = poly.exponents
        polys[idx] = poly.from_attributes(
            exponents=exponents,
            coefficients=poly.coefficients,
            indeterminants=common_indeterminants,
            clean=False,
        )

    return tuple(polys)


def align_exponents(*polys):
    """
    Align polynomials such that the exponents are the same.

    Aligning exponents assumes that the indeterminants is also aligned.

    Args:
        polys (numpoly.ndpoly):
            Polynomial to make adjustment to.

    Returns:
        (Tuple[numpoly.ndpoly, ...]):
            Same as ``polys``, but internal adjustments made to make them
            compatible for further operations.

    Examples:
        >>> x, y = numpoly.symbols("x y")
        >>> poly1 = x*y
        >>> poly2 = numpoly.polynomial([x**5, y**3-1])
        >>> print(poly1.exponents)
        [[1 1]]
        >>> print(poly2.exponents)
        [[0 0]
         [0 3]
         [5 0]]
        >>> poly1, poly2 = numpoly.align_exponents(poly1, poly2)
        >>> print(poly1)
        x*y
        >>> print(poly2)
        [x**5 -1+y**3]
        >>> print(poly1.exponents)
        [[0 0]
         [0 3]
         [1 1]
         [5 0]]
        >>> print(poly2.exponents)
        [[0 0]
         [0 3]
         [1 1]
         [5 0]]

    """
    polys = [numpoly.aspolynomial(poly) for poly in polys]
    if not all(
            polys[0].names == poly.names
            for poly in polys
    ):
        polys = list(align_indeterminants(*polys))

    global_exponents = sorted({
        tuple(exponent) for poly in polys for exponent in poly.exponents})
    for idx, poly in enumerate(polys):
        lookup = {
            tuple(exponent): coefficient
            for exponent, coefficient in zip(
                poly.exponents, poly.coefficients)
        }
        zeros = numpy.zeros(poly.shape, dtype=poly.dtype)
        coefficients = [lookup.get(exponent, zeros)
                        for exponent in global_exponents]
        polys[idx] = poly.from_attributes(
            exponents=global_exponents,
            coefficients=coefficients,
            indeterminants=poly.names,
            clean=False,
        )
    return tuple(polys)
