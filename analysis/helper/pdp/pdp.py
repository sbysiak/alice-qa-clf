import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def compute_pdp(score_func, feat_name, X, y=None, quantiles_range=[0, 1], n_grid_points=50, scaler=None):
    """computes partial dependence

    Parameters
    ----------
    scaler : sklearn.preprocessing.StandardScaler or None
        scaler obj to compute inverse transformation of `X`
        if None, then no transformation of X is computed

    Returns
    -------
    grid : array, shape [n_grid_points]
        values of `feat_name` for which partial dependece was computed
        (x axis for pdp)
    aver_score : array, shape [n_grid_points]
        average score for samples with inputed values of `feat_name`
        (y axis for pdp)
    """
    X_temp = X.copy()
    orig_values = X_temp[feat_name].copy()
    orig_score   = score_func(X_temp, y)

    grid = np.linspace(np.quantile(X_temp[feat_name], quantiles_range[0]),
                       np.quantile(X_temp[feat_name], quantiles_range[1]),
                       n_grid_points)

    rug_locs = [x for x in X_temp[feat_name] if x > grid[0] and x < grid[-1]]
    percentiles = np.quantile(rug_locs, np.linspace(0,1,101))

    scores = np.zeros([X.shape[0], n_grid_points])
    for i, val in enumerate(grid):
        X_temp[feat_name] = val
        scores[:,i] = score_func(X_temp, y)

        if not i % 5: print(i, end=', ')
    print()

    if scaler:
        feat_id = X.columns.tolist().index(feat_name)
        def transform_back(a, feat_id=feat_id, scaler=scaler, n_columns=X.shape[1]):
            a_mat = np.zeros([len(a), n_columns])
            a_mat[:, feat_id] = a
            a_mat_tr = scaler.inverse_transform(a_mat)
            a_tr = a_mat_tr[:, feat_id]
            return a_tr
        grid        = transform_back(grid)
        rug_locs    = transform_back(rug_locs)
        percentiles = transform_back(percentiles)
        orig_values = transform_back(orig_values)

    result = dict(grid=grid, scores=scores, rug_locs=rug_locs, percentiles=percentiles,
                  orig_values=orig_values, orig_score=orig_score)
    return result



def plot_pdp(pdp_result,
             plot_aver=True,
             instance_to_highlight=None,
             plot_rugs=True,
             centered=True, percentile_center_at=50,
             plot_lines=False, lines_frac_to_plot=0.1,
             plot_errorband=True, errorband_nsigma=2,
             highlight_kwargs=dict(),
             ax=None):

    grid        = pdp_result['grid']
    score       = pdp_result['scores']
    percentiles = pdp_result['percentiles']
    rug_locs    = pdp_result['rug_locs']

    if centered:
        shift_index = np.argmin( abs(grid - percentiles[percentile_center_at]) )
        shift_by = score[:,shift_index]
        score = (score.transpose() - shift_by.transpose()).transpose()
    means = score.transpose().mean(axis=1)
    stds = score.transpose().std(axis=1)

    if not ax: fig,ax = plt.subplots(figsize=(10,6))

    if plot_errorband:
        ax.fill_between(grid, means-errorband_nsigma*stds, means+errorband_nsigma*stds, color='#F0F0FF')
        ax.plot(grid, np.array([means-errorband_nsigma*stds, means+errorband_nsigma*stds]).transpose(), color='#BBBBFF')

    if plot_lines:
        if lines_frac_to_plot < 1:
            n_lines_to_plot = int(lines_frac_to_plot * score.shape[0])
        else:
            n_lines_to_plot = lines_frac_to_plot
        rand_lines = np.random.randint(0, score.shape[0], n_lines_to_plot)
        ax.plot(grid, score[rand_lines,:].transpose(), '-', color='k', alpha=0.2, lw=1)

    if plot_aver:
        ax.plot(grid, means, '-', lw=7, color='yellow')
        ax.plot(grid, means, '.-', lw=0.5, color='k')

    if instance_to_highlight:
        ax.plot(grid, score[instance_to_highlight,:].transpose(), '-', lw=10, color='cyan')
        ax.plot(grid, score[instance_to_highlight,:].transpose(), '.-', lw=1.5, color='k')

    if plot_rugs:
        y_min, y_max = ax.get_ylim()
        y_range = y_max - y_min
        rug_y_min = y_min-0.05*y_range
        rug_y_max = rug_y_min + 0.05*(y_max-y_min)
        ax.vlines(rug_locs, rug_y_min, rug_y_max, alpha=0.2)
        ax.set_ylim([rug_y_min, y_max])
    ax.grid(c='#AAAAAA')
    return ax



def plot_ice(pdp_result, instance_to_highlight, **kwargs):

    default_kwargs=dict(
             plot_aver=False,
             plot_rugs=True,
             centered=False, percentile_center_at=50,
             plot_lines=False, lines_frac_to_plot=0.1,
             plot_errorband=False, errorband_nsigma=2,
    )

    for k,v in default_kwargs.items():
        if k not in kwargs.keys():
            kwargs[k] = v
    kwargs['instance_to_highlight'] = instance_to_highlight

    ax = plot_pdp(pdp_result, **kwargs)

    grid        = pdp_result['grid']
    score       = pdp_result['scores']
    percentiles = pdp_result['percentiles']
    orig_values = pdp_result['orig_values']
    orig_score   = pdp_result['orig_score']

    percentile_center_at = kwargs['percentile_center_at']

    if kwargs['centered']:
        shift_index = np.argmin( abs(grid - percentiles[percentile_center_at]) )
        shift_by  = score[:,shift_index]
        orig_score = (orig_score.transpose() - shift_by.transpose()).transpose()

    val  = orig_values[instance_to_highlight]
    pred = orig_score[instance_to_highlight]
    ax.scatter(val, pred, marker='*', s=500, color='red', zorder=1000)

    return ax
