# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot

def interp_nan(tvar, new_tvar='tvar_interp_nan', s_limit=0):
    """
    Interpolates the tplot variable through NaNs in the data.

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions.  If there are more, they may become flattened!

    Parameters:
        tvar : str
            Name of tplot variable.
        s_limit : int or float, optional
            The maximum size of the gap in seconds to not interpolate over.  I.e. if there are too many NaNs in a row, leave them there.
        new_tvar : str
            Name of new tvar for added data.  If not set, then a name is made up.

    Returns:
        None

    Examples:
        >>> # Interpolate through the np.NaN values
        >>> pytplot.store_data('e', data={'x':[2,5,8,11,14,17,21], 'y':[[np.nan,1,1],[np.nan,2,3],[4,np.nan,47],[4,np.nan,5],[5,5,99],[6,6,25],[7,np.nan,-5]]})
        >>> pytplot.interp_nan('e','e_nonan',s_limit=5)
        >>> print(pytplot.data_quants['e_nonan'].values)
    """

    if new_tvar=='tvar_interp_nan':
        newtvar = tvar +"_interp_nan"

    if 'spec_bins' in pytplot.data_quants[tvar].coords:
        d, s = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar)
    else:
        d = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar)
        s = None
    tv1 = d.values.copy()
    tv1 = tv1.astype(float)
    cadence = tv1.index[1] - tv1.index[0]
    n_nans = int(round(s_limit/cadence))
    if s_limit == 0:
        tv1 = tv1.interpolate(method='linear')
    else:
        tv1 = tv1.interpolate(method='linear',limit=n_nans,limit_direction='both') 
    tv1 = tv1.astype(object)

    if s is not None:
        pytplot.store_data(newtvar,data = {'x':tv1.index,'y':tv1, 'v': pytplot.data_quants[tvar].coords['spec_bins'].values})
    else:
        pytplot.store_data(newtvar, data={'x': tv1.index, 'y': tv1})
    return