"""This file contains helper python functions used in the Snakefile.

"""

from pathlib import Path


def get_samples(fastqdir):
    """Given a path `fastqdir` returns a dictionary `samples`, such that
    `samples[sample_name][1]` (or `2`) is a list of files containing
    R1 or R2 respectively.

    """

    if not Path(fastqdir).is_dir():
        raise Exception(f"""{fastqdir} does not exist""")

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

    if not samples:
        raise Exception("Could not find any samples")

    return samples


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


def get_mode(config, samples):
    if "mode" in config:
        mode = config['mode']
    else:
        mode = "auto"

    if mode not in ["single", "paired", "auto"]:
        raise Exception(
            """`mode` must be either "single", "paired" or "auto" """)
    if mode == "auto":
        # check if read 2 exists for all files.  If at least one
        # R1 has no associated R2 switch to single end mode
        for sample in samples:
            for R2 in samples[sample]["2"]:
                if not Path(R2).is_file():
                    return "single"
        return "paired"
    else:
        return mode


def parse_config(config, samples):
    """Re-formats the config to include the automatically determined
files."""

    config['metadir'] = str(get_metadir(config))
    config['fasta'] = str(get_reference_file(config, key="fasta").name)
    config['gtf'] = str(get_reference_file(config, key="gtf").name)
    config['mode'] = get_mode(config, samples)
    return config


def hisat2_input(wildcards, mode):
    """Selects between either a single or paired input based on the
mode"""

    sample = wildcards.sample
    R1, R2 = [f"""trimmed/{mode}/{sample}_R1.fastq""",
              f"""trimmed/{mode}/{sample}_R2.fastq"""]

    if mode == "single":
        return [R1]
    elif mode == "paired":
        return [R1, R2]
