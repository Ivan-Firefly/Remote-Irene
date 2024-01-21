# Тонкий клиент для голосового ассистента [Ирины](https://github.com/janvarev/Irene-Voice-Assistant)


Отличие от оригинального репозитория:
1. `run_remoteva_micrem.py` - вынес выбор микрофона `deviceId` и частоту `samplerateMic` в `options.json`
2. `play_wav.py` - заменил библиотеку на sounddevice (audioplayer почему-то не заработал на Linux)
3. `run_remoteva_voskrem.py` - добавлен вывод доступных аудиоустройств перед запуском клиента

**`deviceId` НЕ может быть пустым!**

Образ - https://hub.docker.com/r/firefly27/irene-mic-client

Запускать удобнее через `docker-compose.yml`. Перед запуском положить `options.json` рядом с `docker-compose.yml` и изменить адрес сервера с Ириной (остальные параметры по желанию).

**Docker версия основного сервера:**

https://github.com/Ivan-Firefly/Irene-Voice-Assistant-Docker
