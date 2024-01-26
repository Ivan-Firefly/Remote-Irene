FROM python:3.10-slim

RUN --mount=type=cache,target=/var/cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libportaudio2 \
    libffi-dev \
    libsndfile1-dev \
    cmake \
    build-essential

COPY run_remoteva_micrem.py \
     requirements-docker.txt \
     run_remoteva_voskrem.py \
     play_wav.py \
     save_wav.py \
     options.json \
     run_remote_telegrambot.py \
     options_telegrambot.json \
     run_remoteva_cmdline.py \
     jaa.py /

RUN pip install -r ./requirements-docker.txt

CMD sh -c "python3 run_remoteva_voskrem.py"
