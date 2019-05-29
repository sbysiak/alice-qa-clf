from ipywidgets import interact, interactive, fixed


def show_qa_plots(row_orig, plot_select='all'):
    """shows in notebook TPC-QA plots available in web

    Parameters
    ----------
    row_orig : pandas.core.series.Series object
        row of dataframe from a loaded csv file,
        containing fields: 'year', 'period.fString', 'pass.String', 'run'
        e.g. result of `df.iloc[instance_index]`

    plot_select : string
        name of plot to be selected or 'all'
        default='all', meaning Dropdown widget with all available plots
    """
    from IPython.display import Markdown as md
    available_plots = [('Event Information', 'TPC_event_info.png'), ('Cluster Occupancy', 'cluster_occupancy.png'), ('#eta, #phi and pt', 'eta_phi_pt.png'), ('Number of clusters in #eta and #phi', 'cluster_in_detail.png'), ('DCAs vs #eta', 'dca_in_detail.png'), ('TPC dEdx', 'TPC_dEdx_track_info.png'), ('DCAs vs #phi', 'dca_and_phi.png'), ('TPC-ITS matching', 'TPC-ITS.png'), ('dcar vs pT', 'dcar_pT.png'), ('Tracking parameter phi', 'pullPhiConstrain.png'), ('Raw QA Information', 'rawQAInformation.png'), ('Canvas ROC Status OCDB', 'canvasROCStatusOCDB.png'), ('Resolution vs pT and 1/pT', 'res_pT_1overpT.png'), ('Efficiency all charged + findable', 'eff_all+all_findable.png'), ('Efficiency #pi, K, p', 'eff_Pi_K_P.png'), ('Efficiency findable #pi, K, p', 'eff_Pi_K_P_findable.png')]
    file_names_mapping = dict(available_plots)

    path = '/'.join([str(el) for el in row_orig[['year', 'period.fString', 'pass.fString', 'run']].to_list()])
    path = path.replace('pass1/', 'pass1/000')

    def show_single_plot(plot_name, path=path, file_names_mapping=file_names_mapping):
        plot_file_name = file_names_mapping[plot_name]
        src = f"http://aliqatpceos.web.cern.ch/aliqatpceos/data/{path}/{plot_file_name}"
        html = f'<img src={src} width="1200" height="1200">'
        print(src)
        return md(html)

    if plot_select == 'all':
        plot_name = file_names_mapping.keys()
    else:
        plot_name = plot_select

    interact(show_single_plot, plot_name=plot_name,
             path=fixed(path), file_names_mapping=fixed(file_names_mapping))
