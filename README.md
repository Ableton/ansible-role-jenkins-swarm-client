Ansible role ableton.jenkins_swarm_client
=========================================

This role installs the [Jenkins Swarm Client][jenkins-swarm-client] as a service on the
given host, which allows it to connect to a Jenkins controller instance as a build node.

Requirements
------------

This role requires Ansible >= 2.10 on the Ansible control host, and Java >= 8 to be
installed on the host itself. This role does **not** install Java; this should be done
separately either with another role or via the respective package manager for the host's
platform. This role supports the following platforms:

- Linux (Debian-flavored)
- macOS
- Windows 8.1 or 10

Role Variables
--------------

The following variables must be defined before attempting to apply this role:

- `jenkins_config_group`: The group which `jenkins_config_owner` belongs to. **Note**:
  this group is only created if the `swarm_client_create_user` variable is `true`.
- `jenkins_config_owner`: The user who the Swarm Client will run under. **Note**: this
  user is only created if the `swarm_client_create_user` variable is `true`.
- `jenkins_controller_url`: URL for the Jenkins controller.
- `jenkins_swarm_home`: Path to use for the Swarm Client home. Aside from
  containing the Swarm Client software, this directory will also be used for the
  build's workspace. Therefore, you should take care that the partition this path is on
  has sufficient hard disk space to handle build artifacts and such.
- `swarm_client_create_user`: If true, then create the user/group specified by
  `jenkins_config_owner`/`jenkins_config_group`. If false, then the role assumes that this
  user already exists (default value: `true`).

This role also defines a dict variable, `jenkins_swarm_config_args`, which may contain
values for the swarm client's [YAML configuration file][swarm-client-yaml-config]. See the
[`defaults/main.yml`](defaults/main.yml) file for full documentation on required and
optional role variables.

Example Playbook
----------------

```yaml
---
- name: Install Jenkins Swarm Client on hosts
  hosts: "all"
  vars:
    jenkins_config_group: "jenkins"
    jenkins_config_user: "{{ ansible_user }}"
    jenkins_controller_url: "https://jenkins.example.com"
    jenkins_swarm_home: "/node/build/jenkins"

    # These arguments will be used to construct the Swarm Client's YAML config file
    jenkins_swarm_config_args:
      disableClientsUniqueId: true
      deleteExistingClients: true
      environmentVariables:
        FOO: "BAR"
      executors: 1
      fsroot: "{{ jenkins_swarm_home }}"
      labels:
        - "{{ inventory_hostname }}"
        - "some-other-extra-label"
      mode: "exclusive"
      prometheusPort: 8100

  roles:
    - ableton.jenkins_swarm_client
```

License
-------

MIT

Maintainers
-----------

This project is maintained by the following GitHub users:

- [@ala-ableton](https://github.com/ala-ableton)
- [@nre-ableton](https://github.com/nre-ableton)


[jenkins-swarm-client]: https://plugins.jenkins.io/swarm
[swarm-client-yaml-config]: https://github.com/jenkinsci/swarm-plugin/blob/master/docs/configfile.adoc
