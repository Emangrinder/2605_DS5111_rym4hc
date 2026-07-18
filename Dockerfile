# Step 1: Initialize environment using an official light-weight base image
FROM python:3.12-slim

# Step 2: Establish the working environment directory inside the container
ARG APP_DIR=/app
WORKDIR ${APP_DIR}
ENV PYTHONPATH=${APP_DIR}

# Step 3: Copy only dependency manifests first to maximize layer caching benefits
COPY requirements.txt .

# Step 4: Install runtime python dependencies cleanly without system caching bloating the layer
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy your functional codebase assets down into the image space
COPY bin/ ./bin/
COPY lib/ ./lib/
RUN mkdir -p logs/

# Step 6: Default entrypoint chains the full pipeline end-to-end:
# format-filter -> raw extraction -> Gemini enrichment -> Snowflake load,
# so a plain docker run with no command override delivers records.
CMD ["sh", "-c", "python bin/clean_ids.py | python bin/extract_transcripts.py | python bin/enrich_transcripts.py | python bin/load_snowflake.py"]
