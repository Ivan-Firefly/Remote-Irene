FROM python:3.10-slim

RUN --mount=type=cache,target=/var/cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libportaudio2 \
    libffi-dev \
    libsndfile1-dev

COPY run_remoteva_micrem.py /.
COPY requirements-docker.txt /requirements.txt
COPY run_remoteva_voskrem.py /.
COPY play_wav.py /.
COPY save_wav.py /.
COPY options.json /.
COPY run_remote_telegrambot.py /.
COPY options_telegrambot.json /.
COPY run_remoteva_cmdline.py /.
COPY jaa.py /.

RUN pip install -r requirements.txt

CMD sh -c "python3 run_remoteva_voskrem.py & python3 run_remote_telegrambot.py"
