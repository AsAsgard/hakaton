FROM archlinux/base

MAINTAINER AsAsgard

RUN pacman -Sy --noconfirm python-pip
RUN pacman -Sy --noconfirm cronie

ENV TZ=Europe/Moscow
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

COPY . /vk_bot

WORKDIR /vk_bot
RUN pwd

RUN pip install -r ./requirements/production.txt

CMD ["python", "manage.py"]
