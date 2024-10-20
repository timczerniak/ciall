## BASE TARGET
# Use base python3.12 image with Debian 'Bookworm'
FROM python:3.12.0-bookworm AS ciall_base
COPY ./requirements.txt reqs/requirements.txt
WORKDIR /reqs
RUN apt-get update && \
    apt-get install -y make
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt
#####

## TESTBASE TARGET
FROM ciall_base AS ciall_testbase
# Copy the directory
COPY . /ciall
# run the tests
WORKDIR /ciall
####