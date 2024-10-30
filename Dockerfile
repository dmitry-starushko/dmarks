FROM archlinux:latest
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
RUN pacman -Suy --noconfirm
RUN pacman -S coreutils base-devel boost-libs postgresql-libs python python-pip --noconfirm
RUN pip install --upgrade pip --break-system-packages --root-user-action=ignore
RUN pip install -r addons/requirements.txt --break-system-packages --root-user-action=ignore
