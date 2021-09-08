"""Molecule tests for the default scenario."""

import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_jenkins_user(host):
    """Test that the Jenkins user was created."""
    user = host.user("juser")

    assert user.group == "jgroup"
    assert user.home == "/jenkins"
    assert user.shell == "/bin/bash"


def test_jenkins_dir(host):
    """Test that the Jenkins directory was created."""
    jenkins_dir = host.file("/jenkins")

    assert jenkins_dir.is_directory
    assert jenkins_dir.mode == 0o0755
    assert jenkins_dir.user == "juser"
    assert jenkins_dir.group == "jgroup"


def test_jenkins_swarm_client_config_files(host):
    """Test that Swarm Client configuration files were created."""
    swarm_client_config_file = host.file("/jenkins/swarm-client-config.yml")
    logging_config_file = host.file("/jenkins/logging.properties")

    assert swarm_client_config_file.is_file
    assert logging_config_file.is_file


def test_swarm_client_running(host):
    """Test that the Swarm Client service was started."""
    process = host.process.get(comm="java")

    assert process is not None
    assert process.args == " ".join(
        [
            "/usr/bin/java",
            "-Djava.util.logging.config.file=/jenkins/logging.properties",
            "-jar",
            "/jenkins/swarm-client-3.27.jar",
            "-config",
            "/jenkins/swarm-client-config.yml",
        ]
    )
