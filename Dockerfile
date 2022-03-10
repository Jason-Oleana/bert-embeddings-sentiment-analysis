FROM jupyter/base-notebook:python-3.8.8

# Set working directory
WORKDIR /work

# Copy notebook-requirements.txt in working directory
COPY ./notebooks/notebook-requirements.txt ./

# Pip install -r requirements.txt
RUN pip install -r notebook-requirements.txt --no-cache-dir

# Copy dataset directory in working directory
COPY ./dataset ./dataset

# Copy models directory in working directory
COPY ./models ./models

# Copy notebooks directory in working directory
COPY ./notebooks/BERT_mlp_model.ipynb ./notebooks/BERT_mlp_model.ipynb