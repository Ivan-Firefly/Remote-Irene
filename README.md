# Тонкий клиент для голосового ассистента [Ирины](https://github.com/janvarev/Irene-Voice-Assistant)


Отличие от оригинального репозитория:
1. `play_wav.py` - заменил библиотеку на sounddevice (audioplayer почему-то не заработал на Linux)
2. `run_remoteva_voskrem.py` -  вынес выбор микрофона `deviceId` и частоту `samplerateMic` в `options.json`. Добавлен вывод доступных аудиоустройств перед запуском клиента. Убраны неиспользуемые библиотеки.

**`deviceId` НЕ может быть пустым!**

Образ - https://hub.docker.com/r/firefly27/remote-irene-docker

Запускать удобнее через `docker-compose.yml`. Перед запуском положить `options.json` рядом с `docker-compose.yml` и изменить адрес сервера с Ириной(в локльной сети типа `192.168.0.15`), остальные параметры по желанию.

**Docker версия основного сервера:**

https://github.com/Ivan-Firefly/Irene-Voice-Assistant-Docker
