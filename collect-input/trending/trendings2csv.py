import uproot
o = uproot.open('../OUTPUTS/data/2018/LHC18d/MERGED_TRENDING.root')
t = o['tpcQA']
df = t.pandas.df()

for c in df.columns:
    if type(df[c][1]).__module__ not in ['numpy', 'builtins']: df = df.drop(c, axis=1)
