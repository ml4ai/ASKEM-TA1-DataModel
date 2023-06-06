# Start from the python image
FROM python:3.9-bullseye
# Set up the workdir and copy the environment
WORKDIR /app
COPY . /app
RUN mkdir /data
RUN chmod a+rw /data
# Create the virtual environment and install dependencies
ENV VIRTUAL_ENV=/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="/app:$VIRTUAL_ENV/bin:$PATH"

RUN . venv/bin/activate && \
    python -m pip install --upgrade pip && \
    python -m pip install pydantic &&  \
    python -m pip install "."

# Move scripts around for convenience
RUN mv bin/* .
RUN chmod u+x normalize_extractions.sh

CMD ["/bin/bash", "./normalize_extractions.sh"]