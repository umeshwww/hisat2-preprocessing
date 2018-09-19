import pandas as pd
from pathlib import Path
from functools import reduce

dfs = []
for f in snakemake.input:
    sample = Path(f).stem
    df = pd.read_csv(f, sep='\t', index_col=0, names=["EnsembleID", sample])
    dfs.append(df)

df_final = reduce(lambda left, right: pd.merge(left, right, on='EnsembleID'), dfs)

df_final.to_csv(snakemake.output[0], sep='\t')
