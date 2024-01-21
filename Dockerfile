FROM python:3.10-slim

# RUN apk add --no-cache build-base portaudio-dev libffi-dev libsndfile1-dev
RUN --mount=type=cache,target=/var/cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    # build-base \
    # portaudio-dev \
    libportaudio2 \
    libffi-dev \
    libsndfile1-dev

COPY run_remoteva_micrem.py /.
COPY requirements-docker.txt /requirements.txt
COPY run_remoteva_voskrem.py /.
COPY play_wav.py /.
COPY save_wav.py /.
COPY options.json /.

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python run_remoteva_voskrem.py"]
