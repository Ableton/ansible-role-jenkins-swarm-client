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

- `jenkins_master_url`: URL to the Jenkins master instance.
- `jenkins_swarm_home`: Path to use for the Swarm Client home. Aside from
  containing the Swarm Client software, this directory will also be used for the
  build `workspace`.

This role defines the following variables, which may be overridden if
desired:

- `jenkins_node_name`: The name of the node to display in Jenkins. Note that
  Jenkins will add a unique postfix to this name. Default value is
  `inventory_hostname`.
- `jenkins_node_label`: A label to add to the node. Note that the Swarm Client
  plugin will add the `swarm` label to all nodes.


Example Playbook
----------------

```
- name: Get info for Jenkins controller
  hosts: "{{ host | default('nodes') }}"
  tasks:
    - set_fact:
        jenkins_master_url: "http://jenkins.example.com"

- name: Provision Jenkins node
  hosts: "{{ host | default('nodes') }}"
  vars:
    - jenkins_swarm_home: "/tmp/jenkins-node"
  roles:
    - ableton.jenkins-swarm-client
```


[jenkins-swarm-client]: https://plugins.jenkins.io/swarm
