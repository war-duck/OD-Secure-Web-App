FROM archlinux:latest

EXPOSE 8080
RUN pacman -Sy
RUN pacman-key --init && pacman-key --populate archlinux
RUN pacman -S archlinux-keyring --noconfirm
RUN pacman -Syu --noconfirm

RUN pacman -S --noconfirm python python-pip uwsgi uwsgi-plugin-python gcc nginx

WORKDIR /app
COPY . .
RUN python3 -m venv venv
RUN source venv/bin/activate && pip3 install -r requirements.txt
