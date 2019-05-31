# Set the base image for preprocess tools
FROM pguen/bioinfo-base-image:pg_v1.0

# File Author / Maintainer
MAINTAINER Paweł Biernat <pawel.biernat@gmail.com>

# necessary for multiqc
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# the data-dumper is required by the gtf2bed script, which in turn is
# required by the rseqc (apparently rseqc does not work with bed files
# generated with standard tools like BEDOPS).

RUN apt-get update &&\
    apt-get install -y --no-install-recommends libdata-dumper-simple-perl lolcat figlet cowsay &&\
    apt-get clean

#TODO: Retest this with latest version on conda. See if pip dependancy can be eliminated.
# the newest version on conda is 0.9.1 but it has some kind of bug
# that prevented me from using it on my test files.  The pip version
# works fine though.
RUN pip install htseq==0.11.0

COPY config /config
COPY scripts /scripts

# the snakemake command to run the pipeline
ENTRYPOINT ["snakemake", "--directory", "/output", "--snakefile", "/scripts/Snakefile", "-p", "--jobs", "8"]
CMD ["all"]
