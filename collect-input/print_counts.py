import pickle
import pprint

pp = pprint.PrettyPrinter(indent=4)
r = pickle.load(open('counts.pickle'))


pp.pprint(r)
print('\n'*10)

for year in r.keys():
    for period in r[year]:
        r[year][period]['<ALL_APPROX>'] = {}
        for ftype in ['esd', 'qa']:
            n_all = r[year][period]['<ALL>'][ftype]
            if   n_all >= 0: r[year][period]['<ALL_APPROX>'][ftype] = n_all
            else:
                n_collected = sum( [1 for run in r[year][period].keys() if run.startswith('000')] ) 
                scale_factor = float( r[year][period]['n_runs'] ) / n_collected
                sum_collected = sum( [v[ftype] for k,v in r[year][period].items() if k not in ['<ALL>', 'n_runs', '<ALL_APPROX>']] )
                r[year][period]['<ALL_APPROX>'][ftype] = sum_collected * scale_factor


for year in sorted(r.keys()):
    for period in sorted(r[year]):
        n = r[year][period]['<ALL_APPROX>']
        n_qa = str(n['qa']) if isinstance(n['qa'], int) else '~ {:.0f}'.format( round(n['qa'], -3) )
        n_esd = str(n['esd']) if isinstance(n['esd'], int) else '~ {:.0f}'.format( round(n['esd'], -3) )
        frac = '{:.0f} %'.format(100.*n['qa']/n['esd']) if n['esd'] > 0 else 'N/A'
        print '{} | {:>12s} QAs  |  {:>12s} ESDs | {:>5s}'.format(period, n_qa, n_esd, frac )
    print '- -'*18
