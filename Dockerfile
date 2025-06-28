FROM ubuntu:24.04

#
# build with
# docker build --tag marksivill/mcp-spectral:latest --progress=plain --no-cache .
# docker run marksivill/mcp-spectral:latest
#

#
# Install Python 3.13 ( which calls spectral via command line )
# Install Spectral ( requires node )
#
RUN apt-get update \
    && apt-get install -y \           
    software-properties-common \
    curl \
    && add-apt-repository ppa:deadsnakes/ppa \
    && curl -fsSL https://deb.nodesource.com/setup_22.x -o /tmp/nodesource_setup.sh \
    && bash /tmp/nodesource_setup.sh \   
    && apt-get update \
    && apt-get install -y \
    nodejs \
    python3.13 \
    && npm install -g @stoplight/spectral-cli@6.15.0 \
    && rm -rf /var/lib/apt/lists/*
 
# Set working directory
WORKDIR /app

RUN useradd -m -s /bin/bash appuser \
    && chown -R appuser:appuser /app
    
USER appuser

# install python uv under appuser
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/appuser/.local/bin/:$PATH"

#
# Copy python / yaml project files
#
USER root

COPY requirements.txt .
COPY *.py .
COPY *.yaml .

RUN chown -R appuser:appuser /app

USER appuser

# set up python project
# Verify all components installed
RUN uv init \
    &&  uv add -r requirements.txt \
    && echo "python3 version - `python3 --version`" \
    && echo "uv version - `uv self version`" \
    && echo "node version - `node --version`" \
    && echo "npm version - `npm --version`" \
    && echo "spectral version - `spectral --version`"

# start mcp server 
CMD ["uv", "run", "mcp_spectral.py"]
