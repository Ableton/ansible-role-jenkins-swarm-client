FROM ubuntu:16.04

ARG jenkins_swarm_home
ARG jenkins_user
ARG jenkins_password

RUN apt update
RUN apt install -y openssh-server sudo python
EXPOSE 22
RUN mkdir /var/run/sshd

RUN useradd -d "${jenkins_swarm_home:?}" -m -G ssh,sudo -s /bin/bash "${jenkins_user:?}"
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN echo "${jenkins_user:?}:${jenkins_password:?}" | chpasswd

# This code causes the following hadolint violation
# DL3025 Use arguments JSON notation for CMD and ENTRYPOINT arguments
# Because of the &&, we can't use JSON notation here
CMD /usr/sbin/sshd && sleep infinity
