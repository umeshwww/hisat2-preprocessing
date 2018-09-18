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

# a work around to activate the environment
RUN echo "source activate hisat2" > ~/.bashrc
ENV PATH /usr/local/envs/hisat2/bin:$PATH

# the snakemake command to run the pipeline
CMD ["snakemake", "--directory", "/output","--jobs","4"]
