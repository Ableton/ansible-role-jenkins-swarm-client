Jenkins Swarm Client Role
=========================

This role installs and starts up the [Jenkins Swarm
Client][jenkins-swarm-client] on a host, which will allow it to connect to a
Jenkins controller instance as a build node.

Requirements
------------

This role requires Java 8 to be installed on the host.


Role Variables
--------------

The following variables must be defined before attempting to apply this role:

- `jenkins_controller_url`: URL for the Jenkins controller.
- `jenkins_swarm_home`: Path to use for the Swarm Client home. Aside from
  containing the Swarm Client software, this directory will also be used for the
  build `workspace`.

This role also defines a dict variable, `jenkins_swarm_config_args`, which may contain
values for the swarm client's [YAML configuration file][swarm-client-yaml-config].


Example Playbook
----------------

```
- name: Get info for Jenkins controller
  hosts: "{{ host | default('nodes') }}"
  tasks:
    - set_fact:
        jenkins_controller_url: "http://jenkins.example.com"

- name: Provision Jenkins node
  hosts: "{{ host | default('nodes') }}"
  vars:
    - jenkins_swarm_home: "/tmp/jenkins-node"
  roles:
    - ableton.jenkins_swarm_client
```


[jenkins-swarm-client]: https://plugins.jenkins.io/swarm
[swarm-client-yaml-config]: https://github.com/jenkinsci/swarm-plugin/blob/master/docs/configfile.adoc
