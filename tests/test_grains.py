import re
import pytest
from utils import check_output


pytestmark = pytest.mark.usefixtures("master", "minion_ready")


@pytest.fixture(scope="session")
def os_release(request):
    info = dict()
    with open('/etc/os-release', 'rb') as f:
        info.update(
            dict(
                [it.strip().replace('"', '').split('=') for it in f.readlines()]
            )
        )
    return info


@pytest.fixture(scope="session")
def suse_release(request):
    info = dict()
    with open('/etc/SuSE-release', 'rb') as f:
        for line in f.readlines():
            match = re.match('([a-zA-Z]+)\s*=\s*(\d+)', line)
            if match:
                info.update([match.groups()])
    return info


def test_get_cpuarch(caller_client):
    assert caller_client.cmd('grains.get', 'cpuarch') == 'x86_64'


def test_get_os(caller_client):
    assert caller_client.cmd('grains.get', 'os') == "SUSE"


def test_get_items(caller_client):
    assert caller_client.cmd('grains.get', 'items') == ''


def test_get_os_family(caller_client):
    assert caller_client.cmd('grains.get', 'os_family') == 'Suse'


def test_get_oscodename(env, caller_client, os_release):
    assert caller_client.cmd('grains.get', 'oscodename') == os_release['PRETTY_NAME']


def test_get_osfullname(env, caller_client, os_release):
    assert caller_client.cmd('grains.get', 'osfullname') == os_release['NAME']


def test_get_osarch(env, caller_client):
    expected = check_output(['rpm', '--eval', '%{_host_cpu}']).strip()
    assert caller_client.cmd('grains.get', 'osarch') == expected


def test_get_osrelease(env, caller_client, os_release):
    assert caller_client.cmd('grains.get', 'osrelease') == os_release['VERSION_ID']


def test_get_osrelease_info(env, caller_client, suse_release):
    expected = (int(suse_release['VERSION']), int(suse_release['PATCHLEVEL']))
    assert caller_client.cmd('grains.get', 'osrelease_info') == expected