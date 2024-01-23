FROM python:3.10-slim

# RUN apk add --no-cache build-base portaudio-dev libffi-dev libsndfile1-dev
RUN --mount=type=cache,target=/var/cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libportaudio2 \
    libffi-dev \
    libsndfile1-dev \
    supervisor

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
COPY supervisord.conf /.

RUN pip install -r requirements.txt

CMD ["bash", "-c", "supervisord -n -c supervisord.conf"]
