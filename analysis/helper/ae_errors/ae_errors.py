import numpy as np
import matplotlib.pyplot as plt

DEFAULT_GROUPS_FUNCS = [
                        ('TPC-ITS_match.',  lambda col: 'tpcIts' in col),
                        ('TPC_nclusters',   lambda col: 'TPC' in col),
#                        ('TPC_nclusters',   lambda col: 'TPC' in col and 'slope' not in col),
#                        ('TPC_ncl-fits',    lambda col: 'TPC' in col and 'slope' in col),
                        ('vertex',          lambda col: 'vert' in col.lower()),
                        ('multiplicity',    lambda col: 'Mult' in col),
                        ('pT',              lambda col: ('PtA' in col or 'PtC' in col or 'qOverPt' in col) and 'tpcIts' not in col and 'deltaPt' not in col),
                        ('delta pT',        lambda col: 'deltaPt' in col),
                        ('MIP',             lambda col: ('MIP' in col)),
                        ('distr._pulls',    lambda col: 'Pull' in col),
                        ('work._conditions', lambda col: 'PTR' in col or 'HVandPT' in col or 'VDrift' in col),
                        ('DCA-fits',        lambda col: 'dcar' in col or 'dcaz' in col),
                        ('dZ-fits',         lambda col: 'dZA' in col or 'dZC' in col),
                        ('dR-fits',         lambda col: 'dRA' in col or 'dRC' in col),
                        ('random',          lambda col: 'random' in col)
                        ]

def group_columns(columns, groups_funcs, verbose=False):
    """groups columns according to functions defined in `groups_funcs`

    Parameters
    ----------
    columns : arrays of strings
        column names

    groups_func : list of tuples
        list of pairs:
            group_name
            and
            function returning boolean value if column belong to the group

    verbose : bool

    Returns
    -------
    ordered_columns : array of strings

    groups : list of tuples
        list of pairs:
            group_name
            and
            min and max value of indices of columns belonging to the group
    """
    ordered_columns = []
    groups = dict()

    for group_name, group_func in groups_funcs:
        if verbose:
            print()
            print(group_name, ':\n------', )
        g_min = len(ordered_columns)-1
        for c in columns:
            if group_func(c):
                ordered_columns.append(c)
        g_max = len(ordered_columns)-1
        if g_max > g_min: g_min += 1
        groups[group_name] = (g_min, g_max)

    for col in columns:
        ncounts = ordered_columns.count(col)
        if ncounts > 1:
            raise ValueError(f'a column named {col} appeared in more than one group')
        elif ncounts < 1:
            ordered_columns.append(col)

    return ordered_columns, groups



def plot_AE_error_single(errors, columns, ax, ylabel, groups_funcs):
    """plots barplot with AutoEncoder's errors

    Parameters
    ----------
    errors : array of numeric
        array of error values for each column
    columns : array of strings
        array of column names corresponding to consecutive columns
    ax : matplotlib.axes._subplots.AxesSubplot object
        axes to plot on
    ylabel : string
        label of y-axis
    groups_func :
        passed to `group_columns()`


    Returns
    -------
    ax
    """

    n_bars = len(errors)
    assert n_bars == len(columns)

    ordered_columns, groups = group_columns(columns, groups_funcs=groups_funcs)
    ordered_errors = [errors[list(columns).index(c)] for c in ordered_columns]

    ax.bar(range(n_bars), ordered_errors, width=0.5)
    ax.set_xlim([-1, n_bars+1])
    ax.set_xticks(range(0, n_bars))
    ax.set_xticklabels(labels=ordered_columns, rotation=90, horizontalalignment='center')
    ax.set_ylabel(ylabel, {'fontsize':25})
    ymax = ax.get_ylim()[1]

    for group_name, group_range in groups.items():
        if group_range[1] > group_range[0]:
            ax.vlines([group_range[0]-0.5, group_range[1]+0.5],
                      0, ymax,
                      linestyles='--')
            ax.text(np.mean(group_range), 0.8*ymax,
                    group_name.replace('_', '\n'),
                    horizontalalignment='center', fontdict=dict(fontsize=25),
                    bbox=dict(facecolor='white', edgecolor=None, alpha=0.8))
    return ax



def plot_AE_error(errors, columns, ylabels=None, groups_funcs=DEFAULT_GROUPS_FUNCS, axes=None):
    """plots barplot with AutoEncoder's errors for each error array

    Parameters
    ----------
    errors : 1D or 2D array of numeric
        array(s) of error values for each column
    columns : array of strings
        array of column names corresponding to consecutive columns
    axes : matplotlib.axes._subplots.AxesSubplot object or None
        axes to plot on
        default=None, meaning creating axes inside function
    ylabels : string or array of strings
        labels of y-axes
    groups_func :
        passed to `group_columns()`


    Returns
    -------
    axes
    """
    if isinstance(errors, list): errors = np.array(errors)

    if len(errors.shape) == 2:
        # 2D array -> multiple arrays passed in `errors`
        if not ylabels:
            print('Please provide labels list for y axes')
            ylabels = ['unknown' for _ in errors]
        n_err_arrays = len(errors)
        if axes is None:
            fig, axes = plt.subplots(n_err_arrays, 1, figsize=(50,6*n_err_arrays))
        for err, ylabel, ax in zip(errors, ylabels, axes):
            plot_AE_error_single(err, columns, ax=ax, ylabel=ylabel, groups_funcs=groups_funcs)
        return axes
    elif len(errors.shape) == 1:
        # 1D array -> single array passed in `errors`
        if not ylabels:
            ylabels = 'AE error'
        if axes is None:
            fig, axes = plt.subplots(1,1, figsize=(50,6))
        plot_AE_error_single(errors, columns, ax=axes, ylabel=ylabels, groups_funcs=groups_funcs)
        return axes
