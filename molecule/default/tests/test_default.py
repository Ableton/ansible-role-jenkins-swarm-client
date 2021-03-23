import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_java_installed(host):
    assert host.file('/usr/bin/java').exists


def test_jenkins_user(host):
    user = host.user('juser')

    assert user.group == 'jgroup'
    assert user.home == '/jenkins'
    assert user.shell == '/bin/bash'


def test_jenkins_dir(host):
    jenkins_dir = host.file('/jenkins')

    assert jenkins_dir.is_directory
    assert jenkins_dir.mode == 0o0755
    assert jenkins_dir.user == 'juser'
    assert jenkins_dir.group == 'jgroup'


def test_jenkins_swarm_client_node_labels(host):
    node_labels_file = host.file('/jenkins/node-labels.txt')

    assert node_labels_file.is_file
    assert node_labels_file.content == b'instance node-label extra-label\n'


def test_swarm_client_running(host):
    process = host.process.get(comm='java')

    assert process is not None
    assert process.args == ' '.join([
        '/usr/bin/java',
        '-Djava.util.logging.config.file=/jenkins/logging.properties',
        '-jar',
        '/jenkins/swarm-client-3.22.jar',
        '-master',
        'http://127.0.0.1:8080',
        '-disableClientsUniqueId',
        '-disableSslVerification',
        '-deleteExistingClients',
        '-labelsFile',
        '/jenkins/node-labels.txt',
        '-mode',
        'exclusive',
        '-name',
        'molecule-test-node',
        '-fsroot',
        '/jenkins',
        '-executors',
        '1',
        '-pidFile',
        '/jenkins/swarm-client.pid',
        '-e',
        'FOO=BAR',
    ])
