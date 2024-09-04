# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Set the environment variable
ENV TASK_ROOT /app
# Install Julia and Git
RUN apt-get update && \
    apt-get install -y wget git tar && \
    wget https://julialang-s3.julialang.org/bin/linux/x64/1.9/julia-1.9.0-linux-x86_64.tar.gz && \
    tar xzf julia-1.9.0-linux-x86_64.tar.gz -C /usr --strip-components 1 && \
    rm -rf julia-1.9.0-linux-x86_64.tar.gz
# Install Julia packages

# Create the JULIA_DEPOT_PATH directory
RUN mkdir -p ${TASK_ROOT}/packages

# Set permissions for the JULIA_DEPOT_PATH directory
RUN chmod -R 777 ${TASK_ROOT}/


ENV JULIA_DEPOT_PATH ${TASK_ROOT}/packages

ENV JULIA_CPU_TARGET="generic;Haswell;clone_all"

# Install Julia packages
RUN julia -e 'using Pkg;Pkg.add(["MAT","NIfTI","LsqFit","Statistics","Plots","NaturalSort","Glob"])'
# Copy the current directory contents into the container at /app

# Copy the requirements.txt file into the container
RUN apt-get install -y dcm2niix

COPY . /app
# Copy the requirements.txt file into the container
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


COPY ./OAI_DataProcessing/* /app/


# Install any needed packages specified in requirements.txt


ENTRYPOINT [ "bash", "script.sh" ]
