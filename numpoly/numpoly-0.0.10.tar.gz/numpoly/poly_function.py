"""Polynomial functionality."""
import re
import string

import numpy
import numpoly


def symbols(names="q", asarray=False, dtype="i8"):
    """
    Construct symbol variables.

    Most directly be providing a list of string names. But a set of shorthands
    also exists:

    * ``,`` and `` `` (space) can be used as a variable delimiter.
    * ``{number}:{number}`` can be used to define a numerical range.
    * ``{letter}:{letter}`` can be used to define a alphabet range.

    Args:
        names (str, Tuple[str, ...]):
            Indeterminants are determined by splitting the string on space. If
            iterable of strings, indeterminants defined directly.
        asarray (bool):
            Enforce output as array even in the case where there is only one
            variable.
        dtype (numpy.dtype):
            The data type of the polynomial coefficients.

    Returns:
        (numpoly.ndpoly):
            Polynomial array with unit components in each dimension.

    Examples:
        >>> print(numpoly.symbols("q"))
        q
        >>> print(numpoly.symbols("q,"))
        [q]
        >>> print(numpoly.symbols("q", asarray=True))
        [q]
        >>> print(numpoly.symbols(["alpha", "beta"]))
        [alpha beta]
        >>> print(numpoly.symbols("x y z"))
        [x y z]
        >>> print(numpoly.symbols("a,b,c"))
        [a b c]
        >>> print(numpoly.symbols("q:7"))
        [q0 q1 q2 q3 q4 q5 q6]
        >>> print(numpoly.symbols("q3:6"))
        [q3 q4 q5]
        >>> print(numpoly.symbols("za:f"))
        [za zb zc zd ze zf]

    """
    if not isinstance(names, str):
        names = list(names)

    else:
        names = re.sub(" ", ",", names)
        if "," in names:
            asarray = True
            names = [name for name in names.split(",") if name]

        elif re.search(r"(\d*):(\d+)", names):

            match = re.search(r"(\d*):(\d+)", names)
            start = int(match.group(1) or 0)
            end = int(match.group(2))
            names = [
                names.replace(match.group(0), str(idx))
                for idx in range(start, end)
            ]

        elif re.search(r"([a-zA-Z]+):([a-zA-Z]+)", names):

            match = re.search(r"([a-zA-Z]):([a-zA-Z])", names)
            start = string.ascii_letters.index(match.group(1))
            end = string.ascii_letters.index(match.group(2))
            names = [
                names.replace(
                    match.group(0), string.ascii_letters[idy])
                for idy in range(start, end+1)
            ]

    exponents = numpy.eye(len(names), dtype=int)
    coefficients = numpy.eye(len(names), dtype=dtype)
    if len(names) == 1 and not asarray:
        coefficients = coefficients[0]
    return numpoly.ndpoly.from_attributes(
        exponents=exponents,
        coefficients=coefficients,
        indeterminants=names,
    )


def isconstant(poly):
    """
    Check if a polynomial is constant or not.

    Args:
        poly (numpoly.ndpoly):
            polynomial to check if is constant or not.

    Returns:
        (bool):
            True if polynomial has no indeterminants.

    Examples:
        >>> x = numpoly.symbols("x")
        >>> numpoly.isconstant(numpoly.polynomial([x]))
        False
        >>> numpoly.isconstant(numpoly.polynomial([1]))
        True

    """
    poly = numpoly.aspolynomial(poly)
    for exponent, coefficient in zip(poly.exponents, poly.coefficients):
        if not numpy.any(exponent):
            continue
        if numpy.any(coefficient):
            return False
    return True


def toarray(poly):
    """
    Cast polynomial to numpy.ndarray, if possible.

    Args:
        poly (numpoly.ndpoly):
            polynomial to cast.

    Returns:
        (numpy.ndarray):
            Numpy array.

    Raises:
        ValueError:
            Only constant polynomials can be cast to numpy.ndarray.

    Examples:
        >>> numpoly.polynomial([1, 2]).toarray()
        array([1, 2])
        >>> numpoly.toarray(numpoly.symbols("x"))
        Traceback (most recent call last):
            ...
        ValueError: only constant polynomials can be converted to array.

    """
    poly = numpoly.polynomial(poly)
    if not poly.isconstant():
        raise ValueError(
            "only constant polynomials can be converted to array.")
    return numpy.array(poly.coefficients[0])
