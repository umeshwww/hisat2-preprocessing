"""This file contains helper python functions used in the Snakefile.

"""

from pathlib import Path


def get_samples(fastqdir):
    """Given a path `fastqdir` returns a dictionary `samples`, such that
    `samples[sample_name][1]` (or `2`) is a list of files containing
    R1 or R2 respectively.

    """

    files = Path(fastqdir).glob('**/*_R1_*.fastq.gz')
    samples = dict()

    for f in files:
        sample = f.name.split("_")[0]

        if sample not in samples:
            samples[sample] = {'1': [], '2': []}

            R1 = str(f)
            R2 = str(f).replace("_R1_", "_R2_")

            samples[sample]['1'].append(R1)
            samples[sample]['2'].append(R2)

            return samples

        samples = get_samples("/fastq")


def get_metadir(config):
    """Determines the location of the fasta file.  It will look at the
config file first, if no 'fasta' filed is defined it will look at the index.

    """

    if "metadir" not in config:
        raise Exception("`metadir` not defined in config.yml")
    elif not Path(config["metadir"]).is_dir():
        raise Exception("`metadir` does not point to a directory")
    else:
        return Path(config["metadir"])


def get_reference_file(config, key):
    """Used to determine if the config file points to an actual file (here
key = gtf or fasta). If the respective field is not defined in the
config file it will look for a fasta/gtf file in the `metadir`
directory.

    """

    meta = get_metadir(config)
    if key in config:
        filepath = meta/Path(config[key])
    else:
        files = meta.glob("*.{key}".format(key=key))
        try:
            filepath = next(files)
        except Exception:
            raise Exception(
                "Could not find any {key} files in the {metadir} directory."
                .format(key=key, metadir=meta))
    return filepath


def parse_config(config):
    """Re-formats the config to include the automatically determined
files."""
    config['metadir'] = str(get_metadir(config))
    config['fasta'] = str(get_reference_file(config, key="fasta").name)
    config['gtf'] = str(get_reference_file(config, key="gtf").name)
    return config
