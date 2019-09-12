"""Some useful functions that did not fit into the other modules.
"""

# Builtins
import os
import sys
import math
import logging
import warnings

# External libs
import pandas as pd
import numpy as np
from scipy.ndimage import filters
from scipy.signal import gaussian
from scipy.interpolate import interp1d
import shapely.geometry as shpg
from shapely.ops import linemerge

# Optional libs
try:
    import geopandas as gpd
except ImportError:
    pass

# Locals
import oggm.cfg as cfg
from oggm.cfg import SEC_IN_YEAR, SEC_IN_MONTH
from oggm.utils._downloads import get_demo_file
from oggm.exceptions import InvalidParamsError

# Module logger
log = logging.getLogger('.'.join(__name__.split('.')[:-1]))

_RGI_METADATA = dict()

# Shape factors
# TODO: how to handle zeta > 10? at the moment extrapolation
# Table 1 from Adhikari (2012) and corresponding interpolation functions
_ADHIKARI_TABLE_ZETAS = np.array([0.5, 1, 2, 3, 4, 5, 10])
_ADHIKARI_TABLE_RECTANGULAR = np.array([0.313, 0.558, 0.790, 0.884,
                                        0.929, 0.954, 0.990])
_ADHIKARI_TABLE_PARABOLIC = np.array([0.251, 0.448, 0.653, 0.748,
                                      0.803, 0.839, 0.917])
ADHIKARI_FACTORS_RECTANGULAR = interp1d(_ADHIKARI_TABLE_ZETAS,
                                        _ADHIKARI_TABLE_RECTANGULAR,
                                        fill_value='extrapolate')
ADHIKARI_FACTORS_PARABOLIC = interp1d(_ADHIKARI_TABLE_ZETAS,
                                      _ADHIKARI_TABLE_PARABOLIC,
                                      fill_value='extrapolate')


def parse_rgi_meta(version=None):
    """Read the meta information (region and sub-region names)"""

    global _RGI_METADATA

    if version is None:
        version = cfg.PARAMS['rgi_version']

    if version in _RGI_METADATA:
        return _RGI_METADATA[version]

    # Parse RGI metadata
    reg_names = pd.read_csv(get_demo_file('rgi_regions.csv'), index_col=0)
    if version in ['4', '5']:
        # The files where different back then
        subreg_names = pd.read_csv(get_demo_file('rgi_subregions_V5.csv'),
                                   index_col=0)
    else:
        f = os.path.join(get_demo_file('rgi_subregions_'
                                       'V{}.csv'.format(version)))
        subreg_names = pd.read_csv(f)
        subreg_names.index = ['{:02d}-{:02d}'.format(s1, s2) for s1, s2 in
                              zip(subreg_names['O1'], subreg_names['O2'])]
        subreg_names = subreg_names[['Full_name']]

    # For idealized
    reg_names.loc[0] = ['None']
    subreg_names.loc['00-00'] = ['None']
    _RGI_METADATA[version] = (reg_names, subreg_names)
    return _RGI_METADATA[version]


def query_yes_no(question, default="yes"):  # pragma: no cover
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".

    Credits: http://code.activestate.com/recipes/577058/
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def tolist(arg, length=None):
    """Makes sure that arg is a list."""

    if isinstance(arg, str):
        return [arg]

    try:
        (e for e in arg)
    except TypeError:
        arg = [arg]

    arg = list(arg)

    if length is not None:

        if len(arg) == 1:
            arg *= length
        elif len(arg) == length:
            pass
        else:
            raise ValueError('Cannot broadcast len {} '.format(len(arg)) +
                             'to desired length: {}.'.format(length))

    return arg


def haversine(lon1, lat1, lon2, lat2):
    """Great circle distance between two (or more) points on Earth

    Parameters
    ----------
    lon1 : float
       scalar or array of point(s) longitude
    lat1 : float
       scalar or array of point(s) longitude
    lon2 : float
       scalar or array of point(s) longitude
    lat2 : float
       scalar or array of point(s) longitude

    Returns
    -------
    the distances

    Examples:
    ---------
    >>> haversine(34, 42, 35, 42)
    82633.46475287154
    >>> haversine(34, 42, [35, 36], [42, 42])
    array([ 82633.46475287, 165264.11172113])
    """

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return c * 6371000  # Radius of earth in meters


def interp_nans(array, default=None):
    """Interpolate NaNs using np.interp.

    np.interp is reasonable in that it does not extrapolate, it replaces
    NaNs at the bounds with the closest valid value.
    """

    _tmp = array.copy()
    nans, x = np.isnan(array), lambda z: z.nonzero()[0]
    if np.all(nans):
        # No valid values
        if default is None:
            raise ValueError('No points available to interpolate: '
                             'please set default.')
        _tmp[:] = default
    else:
        _tmp[nans] = np.interp(x(nans), x(~nans), array[~nans])

    return _tmp


def smooth1d(array, window_size=None, kernel='gaussian'):
    """Apply a centered window smoothing to a 1D array.

    Parameters
    ----------
    array : ndarray
        the array to apply the smoothing to
    window_size : int
        the size of the smoothing window
    kernel : str
        the type of smoothing (`gaussian`, `mean`)

    Returns
    -------
    the smoothed array (same dim as input)
    """

    # some defaults
    if window_size is None:
        if len(array) >= 9:
            window_size = 9
        elif len(array) >= 7:
            window_size = 7
        elif len(array) >= 5:
            window_size = 5
        elif len(array) >= 3:
            window_size = 3

    if window_size % 2 == 0:
        raise ValueError('Window should be an odd number.')

    if isinstance(kernel, str):
        if kernel == 'gaussian':
            kernel = gaussian(window_size, 1)
        elif kernel == 'mean':
            kernel = np.ones(window_size)
        else:
            raise NotImplementedError('Kernel: ' + kernel)
    kernel = kernel / np.asarray(kernel).sum()
    return filters.convolve1d(array, kernel, mode='mirror')


def line_interpol(line, dx):
    """Interpolates a shapely LineString to a regularly spaced one.

    Shapely's interpolate function does not guaranty equally
    spaced points in space. This is what this function is for.

    We construct new points on the line but at constant distance from the
    preceding one.

    Parameters
    ----------
    line: a shapely.geometry.LineString instance
    dx: the spacing

    Returns
    -------
    a list of equally distanced points
    """

    # First point is easy
    points = [line.interpolate(dx / 2.)]

    # Continue as long as line is not finished
    while True:
        pref = points[-1]
        pbs = pref.buffer(dx).boundary.intersection(line)
        if pbs.type == 'Point':
            pbs = [pbs]
        elif pbs.type == 'LineString':
            # This is rare
            pbs = [shpg.Point(c) for c in pbs.coords]
            assert len(pbs) == 2
        elif pbs.type == 'GeometryCollection':
            # This is rare
            opbs = []
            for p in pbs:
                if p.type == 'Point':
                    opbs.append(p)
                elif p.type == 'LineString':
                    opbs.extend([shpg.Point(c) for c in p.coords])
            pbs = opbs
        else:
            if pbs.type != 'MultiPoint':
                raise RuntimeError('line_interpol: we expect a MultiPoint '
                                   'but got a {}.'.format(pbs.type))

        # Out of the point(s) that we get, take the one farthest from the top
        refdis = line.project(pref)
        tdis = np.array([line.project(pb) for pb in pbs])
        p = np.where(tdis > refdis)[0]
        if len(p) == 0:
            break
        points.append(pbs[int(p[0])])

    return points


def md(ref, data, axis=None):
    """Mean Deviation."""
    return np.mean(np.asarray(data) - ref, axis=axis)


def mad(ref, data, axis=None):
    """Mean Absolute Deviation."""
    return np.mean(np.abs(np.asarray(data) - ref), axis=axis)


def rmsd(ref, data, axis=None):
    """Root Mean Square Deviation."""
    return np.sqrt(np.mean((np.asarray(ref) - data)**2, axis=axis))


def rmsd_bc(ref, data):
    """Root Mean Squared Deviation of bias-corrected time series.

    I.e: rmsd(ref - mean(ref), data - mean(data)).
    """
    return rmsd(ref - np.mean(ref), data - np.mean(data))


def rel_err(ref, data):
    """Relative error. Ref should be non-zero"""
    return (np.asarray(data) - ref) / ref


def corrcoef(ref, data):
    """Peason correlation coefficient."""
    return np.corrcoef(ref, data)[0, 1]


def nicenumber(number, binsize, lower=False):
    """Returns the next higher or lower "nice number", given by binsize.

    Examples:
    ---------
    >>> nicenumber(12, 10)
    20
    >>> nicenumber(19, 50)
    50
    >>> nicenumber(51, 50)
    100
    >>> nicenumber(51, 50, lower=True)
    50
    """

    e, _ = divmod(number, binsize)
    if lower:
        return e * binsize
    else:
        return (e + 1) * binsize


def signchange(ts):
    """Detect sign changes in a time series.

    http://stackoverflow.com/questions/2652368/how-to-detect-a-sign-change-
    for-elements-in-a-numpy-array

    Returns
    -------
    An array with 0s everywhere and 1's when the sign changes
    """
    asign = np.sign(ts)
    sz = asign == 0
    while sz.any():
        asign[sz] = np.roll(asign, 1)[sz]
        sz = asign == 0
    out = ((np.roll(asign, 1) - asign) != 0).astype(int)
    if asign.iloc[0] == asign.iloc[1]:
        out.iloc[0] = 0
    return out


def polygon_intersections(gdf):
    """Computes the intersections between all polygons in a GeoDataFrame.

    Parameters
    ----------
    gdf : Geopandas.GeoDataFrame

    Returns
    -------
    a Geodataframe containing the intersections
    """

    out_cols = ['id_1', 'id_2', 'geometry']
    out = gpd.GeoDataFrame(columns=out_cols)

    gdf = gdf.reset_index()

    for i, major in gdf.iterrows():

        # Exterior only
        major_poly = major.geometry.exterior

        # Remove the major from the list
        agdf = gdf.loc[gdf.index != i]

        # Keep catchments which intersect
        gdfs = agdf.loc[agdf.intersects(major_poly)]

        for j, neighbor in gdfs.iterrows():

            # No need to check if we already found the intersect
            if j in out.id_1 or j in out.id_2:
                continue

            # Exterior only
            neighbor_poly = neighbor.geometry.exterior

            # Ok, the actual intersection
            mult_intersect = major_poly.intersection(neighbor_poly)

            # All what follows is to catch all possibilities
            # Should not happen in our simple geometries but ya never know
            if isinstance(mult_intersect, shpg.Point):
                continue
            if isinstance(mult_intersect, shpg.linestring.LineString):
                mult_intersect = [mult_intersect]
            if len(mult_intersect) == 0:
                continue
            mult_intersect = [m for m in mult_intersect if
                              not isinstance(m, shpg.Point)]
            if len(mult_intersect) == 0:
                continue
            mult_intersect = linemerge(mult_intersect)
            if isinstance(mult_intersect, shpg.linestring.LineString):
                mult_intersect = [mult_intersect]
            for line in mult_intersect:
                if not isinstance(line, shpg.linestring.LineString):
                    raise RuntimeError('polygon_intersections: we expect'
                                       'a LineString but got a '
                                       '{}.'.format(line.type))
                line = gpd.GeoDataFrame([[i, j, line]],
                                        columns=out_cols)
                out = out.append(line)

    return out


def floatyear_to_date(yr):
    """Converts a float year to an actual (year, month) pair.

    Note that this doesn't account for leap years (365-day no leap calendar),
    and that the months all have the same length.

    Parameters
    ----------
    yr : float
        The floating year
    """

    try:
        sec, out_y = math.modf(yr)
        out_y = int(out_y)
        sec = round(sec * SEC_IN_YEAR)
        if sec == SEC_IN_YEAR:
            # Floating errors
            out_y += 1
            sec = 0
        out_m = int(sec / SEC_IN_MONTH) + 1
    except TypeError:
        # TODO: inefficient but no time right now
        out_y = np.zeros(len(yr), np.int64)
        out_m = np.zeros(len(yr), np.int64)
        for i, y in enumerate(yr):
            y, m = floatyear_to_date(y)
            out_y[i] = y
            out_m[i] = m
    return out_y, out_m


def date_to_floatyear(y, m):
    """Converts an integer (year, month) pair to a float year.

    Note that this doesn't account for leap years (365-day no leap calendar),
    and that the months all have the same length.

    Parameters
    ----------
    y : int
        the year
    m : int
        the month
    """

    return (np.asanyarray(y) + (np.asanyarray(m) - 1) *
            SEC_IN_MONTH / SEC_IN_YEAR)


def hydrodate_to_calendardate(y, m, start_month=None):
    """Converts a hydrological (year, month) pair to a calendar date.

    Parameters
    ----------
    y : int
        the year
    m : int
        the month
    start_month : int
        the first month of the hydrological year
    """

    if start_month is None:
        raise InvalidParamsError('In order to avoid confusion, we now force '
                                 'callers of this function to specify the '
                                 'hydrological convention they are using.')

    e = 13 - start_month
    try:
        if m <= e:
            out_y = y - 1
            out_m = m + start_month - 1
        else:
            out_y = y
            out_m = m - e
    except (TypeError, ValueError):
        # TODO: inefficient but no time right now
        out_y = np.zeros(len(y), np.int64)
        out_m = np.zeros(len(y), np.int64)
        for i, (_y, _m) in enumerate(zip(y, m)):
            _y, _m = hydrodate_to_calendardate(_y, _m, start_month=start_month)
            out_y[i] = _y
            out_m[i] = _m
    return out_y, out_m


def calendardate_to_hydrodate(y, m, start_month=None):
    """Converts a calendar (year, month) pair to a hydrological date.

    Parameters
    ----------
    y : int
        the year
    m : int
        the month
    start_month : int
        the first month of the hydrological year
    """

    if start_month is None:
        raise InvalidParamsError('In order to avoid confusion, we now force '
                                 'callers of this function to specify the '
                                 'hydrological convention they are using.')

    try:
        if m >= start_month:
            out_y = y + 1
            out_m = m - start_month + 1
        else:
            out_y = y
            out_m = m + 13 - start_month
    except (TypeError, ValueError):
        # TODO: inefficient but no time right now
        out_y = np.zeros(len(y), np.int64)
        out_m = np.zeros(len(y), np.int64)
        for i, (_y, _m) in enumerate(zip(y, m)):
            _y, _m = calendardate_to_hydrodate(_y, _m, start_month=start_month)
            out_y[i] = _y
            out_m[i] = _m
    return out_y, out_m


def monthly_timeseries(y0, y1=None, ny=None, include_last_year=False):
    """Creates a monthly timeseries in units of float years.

    Parameters
    ----------
    """

    if y1 is not None:
        years = np.arange(np.floor(y0), np.floor(y1) + 1)
    elif ny is not None:
        years = np.arange(np.floor(y0), np.floor(y0) + ny)
    else:
        raise ValueError("Need at least two positional arguments.")
    months = np.tile(np.arange(12) + 1, len(years))
    years = years.repeat(12)
    out = date_to_floatyear(years, months)
    if not include_last_year:
        out = out[:-11]
    return out


def filter_rgi_name(name):
    """Remove spurious characters and trailing blanks from RGI glacier name.

    This seems to be unnecessary with RGI V6
    """

    if name is None or len(name) == 0:
        return ''

    if name[-1] in ['À', 'È', 'è', '\x9c', '3', 'Ð', '°', '¾',
                    '\r', '\x93', '¤', '0', '`', '/', 'C', '@',
                    'Å', '\x06', '\x10', '^', 'å', ';']:
        return filter_rgi_name(name[:-1])

    return name.strip().title()


def shape_factor_huss(widths, heights, is_rectangular):
    """Shape factor for lateral drag according to Huss and Farinotti (2012).

    The shape factor is only applied for parabolic sections.

    Parameters
    ----------
    widths: ndarray of floats
        widths of the sections
    heights: float or ndarray of floats
        height of the sections
    is_rectangular: bool or ndarray of bools
        determines, whether section has a rectangular or parabolic shape

    Returns
    -------
    shape factor (no units)
    """

    # Ensure bool (for masking)
    is_rect = is_rectangular.astype(bool)
    shape_factors = np.ones(widths.shape)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        shape_factors[~is_rect] = (widths / (2 * heights + widths))[~is_rect]

    shape_factors[heights <= 0.] = 1.

    return shape_factors


def shape_factor_adhikari(widths, heights, is_rectangular):
    """Shape factor for lateral drag according to Adhikari (2012).

    TODO: other factors could be used when sliding is included

    Parameters
    ----------
    widths: ndarray of floats
        widths of the sections
    heights: ndarray of floats
        heights of the sections
    is_rectangular: ndarray of bools
        determines, whether section has a rectangular or parabolic shape

    Returns
    -------
    shape factors (no units), ndarray of floats
    """

    # Ensure bool (for masking)
    is_rectangular = is_rectangular.astype(bool)

    # Catch for division by 0 (corrected later)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        zetas = widths / 2. / heights

    shape_factors = np.ones(widths.shape)

    # TODO: higher order interpolation? (e.g. via InterpolatedUnivariateSpline)
    shape_factors[is_rectangular] = ADHIKARI_FACTORS_RECTANGULAR(
        zetas[is_rectangular])
    shape_factors[~is_rectangular] = ADHIKARI_FACTORS_PARABOLIC(
        zetas[~is_rectangular])

    np.clip(shape_factors, 0.2, 1., out=shape_factors)
    # Set NaN values resulting from zero height to a shape factor of 1
    shape_factors[np.isnan(shape_factors)] = 1.

    return shape_factors
