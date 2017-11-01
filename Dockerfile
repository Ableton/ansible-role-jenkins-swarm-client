FROM ubuntu:17.04

ARG jenkins_swarm_home
ARG jenkins_user
ARG jenkins_password

RUN apt update
RUN apt install -y openssh-server sudo python
EXPOSE 22
RUN mkdir /var/run/sshd

RUN useradd -d $jenkins_swarm_home -m -G ssh,sudo -s /bin/bash $jenkins_user
RUN echo "$jenkins_user:$jenkins_password" | chpasswd

CMD /usr/sbin/sshd && sleep infinity
