# Set the base image to debian based miniconda2
FROM conda/miniconda3

# File Author / Maintainer
MAINTAINER Paweł Biernat <pawel.biernat@gmail.com>

# necessary for multiqc
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# copy and install all the environment
COPY environments /environments

RUN conda env create -f /environments/hisat2.yml

# rseqc is in conflict with multiqc so it get's its own environment
RUN conda env create -f /environments/rseqc.yml

# a work around to activate the environment
RUN echo "source activate hisat2" > ~/.bashrc
ENV PATH /usr/local/envs/hisat2/bin:$PATH

# the newest version on conda is 0.9.1 but it has some kind of bug
# that prevented me from using it on my test files.  The pip version
# works fine though.
RUN pip install htseq==0.11.0

COPY scripts /scripts

# the snakemake command to run the pipeline
ENTRYPOINT ["snakemake", "--directory", "/output", "--snakefile", "/scripts/Snakefile", "-p", "--jobs", "32"]
CMD [""]
