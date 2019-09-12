from io import BytesIO
import logging
import pytest
from typing import List

from .fixtures import MockProvider, MockStorage
from cloudsync.sync.sqlite_storage import SqliteStorage
from cloudsync import Storage, CloudSync, SyncState, SyncEntry, LOCAL, REMOTE, FILE, DIRECTORY, CloudFileNotFoundError, CloudFileExistsError
from cloudsync.event import EventManager

from .test_sync import WaitFor, RunUntilHelper

log = logging.getLogger(__name__)


@pytest.fixture(name="cs")
def fixture_cs(mock_provider_generator):
    roots = ("/local", "/remote")

    class CloudSyncMixin(CloudSync, RunUntilHelper):
        pass

    cs = CloudSyncMixin((mock_provider_generator(), mock_provider_generator()), roots, sleep=None)

    yield cs

    cs.done()

def make_cs(mock_provider_creator, left, right):
    roots = ("/local", "/remote")
    class CloudSyncMixin(CloudSync, RunUntilHelper):
        pass
    return CloudSyncMixin((mock_provider_creator(*left), mock_provider_creator(*right)), roots, sleep=None)

@pytest.fixture(name="multi_cs")
def fixture_multi_cs(mock_provider_generator):
    storage_dict = dict()
    storage = MockStorage(storage_dict)

    class CloudSyncMixin(CloudSync, RunUntilHelper):
        pass

    p1 = mock_provider_generator()
    p2 = mock_provider_generator()
    p3 = mock_provider_generator()

    roots1 = ("/local1", "/remote")
    roots2 = ("/local2", "/remote")

    cs1 = CloudSyncMixin((p1, p2), roots1, storage, sleep=None)
    cs2 = CloudSyncMixin((p1, p3), roots2, storage, sleep=None)

    yield cs1, cs2

    cs1.done()
    cs2.done()


def test_sync_rename_away(multi_cs):
    cs1, cs2 = multi_cs

    remote_parent = "/remote"
    remote_path = "/remote/stuff1"

    local_parent1 = "/local1"
    local_parent2 = "/local2"
    local_path11 = "/local1/stuff1"
    local_path21 = "/local2/stuff1"

    cs1.providers[LOCAL].mkdir(local_parent1)
    cs1.providers[REMOTE].mkdir(remote_parent)
    cs2.providers[LOCAL].mkdir(local_parent2)
    cs2.providers[REMOTE].mkdir(remote_parent)
    linfo1 = cs1.providers[LOCAL].create(local_path11, BytesIO(b"hello1"), None)

    assert linfo1

    cs1.run_until_found(
        (LOCAL, local_path11),
        (REMOTE, remote_path),
        timeout=2)

    cs1.run(until=lambda: not cs1.state.has_changes(), timeout=1)
    cs2.run(until=lambda: not cs2.state.has_changes(), timeout=1)
    log.info("TABLE 1\n%s", cs1.state.pretty_print(use_sigs=False))
    log.info("TABLE 2\n%s", cs2.state.pretty_print(use_sigs=False))

    assert len(cs1.state) == 2      # 1 dirs, 1 files

    # This is the meat of the test. renaming out of one cloud bed into another
    #   Which will potentially forget to sync up the delete to remote1, leaving
    #   the file there and also in remote2
    log.debug("here")
    linfo2 = cs1.providers[LOCAL].rename(linfo1.oid, local_path21)
    log.debug("here")
    cs1.run(until=lambda: not cs1.state.has_changes(), timeout=1)
    log.info("TABLE 1\n%s", cs1.state.pretty_print(use_sigs=False))
    log.debug("here")
    cs2.run(until=lambda: not cs2.state.has_changes(), timeout=1)
    log.info("TABLE 2\n%s", cs2.state.pretty_print(use_sigs=False))
    log.debug("here")

    try:
        cs1.run_until_found(
            WaitFor(LOCAL, local_path11, exists=False),
            timeout=2)
        log.info("TABLE 1\n%s", cs1.state.pretty_print())
        log.info("TABLE 2\n%s", cs2.state.pretty_print())
        cs2.run_until_found(
            (LOCAL, local_path21),
            timeout=2)
        log.info("TABLE 1\n%s", cs1.state.pretty_print())
        log.info("TABLE 2\n%s", cs2.state.pretty_print())
        cs2.run_until_found(
            (REMOTE, remote_path),
            timeout=2)
        log.info("TABLE 1\n%s", cs1.state.pretty_print())
        log.info("TABLE 2\n%s", cs2.state.pretty_print())
        # If renaming out of local1 didn't properly sync, the next line will time out
        cs1.run_until_found(
            WaitFor(REMOTE, remote_path, exists=False),
            timeout=2)
    except TimeoutError:
        log.info("Timeout: TABLE 1\n%s", cs1.state.pretty_print())
        log.info("Timeout: TABLE 2\n%s", cs2.state.pretty_print())
        raise

    # let cleanups/discards/dedups happen if needed
    cs1.run(until=lambda: not cs1.state.has_changes(), timeout=1)
    cs2.run(until=lambda: not cs2.state.has_changes(), timeout=1)

    log.info("TABLE 1\n%s", cs1.state.pretty_print())
    log.info("TABLE 2\n%s", cs2.state.pretty_print())

    assert len(cs1.state) == 1  #  1 dir
    assert len(cs2.state) == 2  #  1 file and 1 dir


def test_sync_multi(multi_cs):
    cs1, cs2 = multi_cs

    local_parent1 = "/local1"
    local_parent2 = "/local2"
    remote_parent1 = "/remote"
    remote_parent2 = "/remote"
    remote_path1 = "/remote/stuff1"
    remote_path2 = "/remote/stuff2"
    local_path11 = "/local1/stuff1"
    local_path21 = "/local2/stuff1"
    local_path12 = "/local1/stuff2"
    local_path22 = "/local2/stuff2"

    cs1.providers[LOCAL].mkdir(local_parent1)
    cs1.providers[REMOTE].mkdir(remote_parent1)
    cs2.providers[LOCAL].mkdir(local_parent2)
    cs2.providers[REMOTE].mkdir(remote_parent2)
    linfo1 = cs1.providers[LOCAL].create(local_path11, BytesIO(b"hello1"), None)
    linfo2 = cs2.providers[LOCAL].create(local_path21, BytesIO(b"hello2"), None)
    rinfo1 = cs1.providers[REMOTE].create(remote_path2, BytesIO(b"hello3"), None)
    rinfo2 = cs2.providers[REMOTE].create(remote_path2, BytesIO(b"hello4"), None)

    assert linfo1 and linfo2 and rinfo1 and rinfo2

    cs1.run_until_found(
        (LOCAL, local_path11),
        (LOCAL, local_path21),
        (REMOTE, remote_path1),
        (REMOTE, remote_path2),
        timeout=2)

    cs1.run(until=lambda: not cs1.state.has_changes(), timeout=1)
    log.info("TABLE 1\n%s", cs1.state.pretty_print())
    log.info("TABLE 2\n%s", cs2.state.pretty_print())

    assert len(cs1.state) == 3      # 1 dirs, 2 files, 1 never synced (local2 file)

    try:
        cs2.run_until_found(
            (LOCAL, local_path12),
            (LOCAL, local_path22),
            (REMOTE, remote_path1),
            (REMOTE, remote_path2),
            timeout=2)
    except TimeoutError:
        log.info("Timeout: TABLE 1\n%s", cs1.state.pretty_print())
        log.info("Timeout: TABLE 2\n%s", cs2.state.pretty_print())
        raise

    linfo12 = cs1.providers[LOCAL].info_path(local_path12)
    rinfo11 = cs1.providers[REMOTE].info_path(remote_path1)
    linfo22 = cs2.providers[LOCAL].info_path(local_path22)
    rinfo21 = cs2.providers[REMOTE].info_path(remote_path1)

    assert linfo12.oid
    assert linfo22.oid
    assert rinfo11.oid
    assert rinfo21.oid
    assert linfo12.hash == rinfo1.hash
    assert linfo22.hash == rinfo2.hash

    # let cleanups/discards/dedups happen if needed
    cs2.run(until=lambda: not cs2.state.has_changes(), timeout=1)
    log.info("TABLE\n%s", cs2.state.pretty_print())

    assert len(cs1.state) == 3
    assert len(cs2.state) == 3


def test_sync_basic(cs):
    local_parent = "/local"
    remote_parent = "/remote"
    remote_path1 = "/remote/stuff1"
    local_path1 = "/local/stuff1"
    remote_path2 = "/remote/stuff2"
    local_path2 = "/local/stuff2"

    cs.providers[LOCAL].mkdir(local_parent)
    cs.providers[REMOTE].mkdir(remote_parent)
    linfo1 = cs.providers[LOCAL].create(local_path1, BytesIO(b"hello"), None)
    rinfo2 = cs.providers[REMOTE].create(remote_path2, BytesIO(b"hello2"), None)

    cs.run_until_found(
        (LOCAL, local_path1),
        (LOCAL, local_path2),
        (REMOTE, remote_path1),
        (REMOTE, remote_path2),
        timeout=2)

    linfo2 = cs.providers[LOCAL].info_path(local_path2)
    rinfo1 = cs.providers[REMOTE].info_path(remote_path1)

    assert linfo2.oid
    assert rinfo1.oid
    assert linfo2.hash == rinfo2.hash
    assert linfo1.hash == rinfo1.hash

    assert not cs.providers[LOCAL].info_path(local_path2 + ".conflicted")
    assert not cs.providers[REMOTE].info_path(remote_path1 + ".conflicted")

    # let cleanups/discards/dedups happen if needed
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)
    log.info("TABLE\n%s", cs.state.pretty_print())

    assert len(cs.state) == 3
    assert not cs.state.has_changes()


def setup_remote_local(cs, *names):
    remote_parent = "/remote"
    local_parent = "/local"

    cs.providers[LOCAL].mkdir(local_parent)
    cs.providers[REMOTE].mkdir(remote_parent)

    found = []
    for name in names:
        remote_path1 = "/remote/" + name
        local_path1 = "/local/" + name
        linfo1 = cs.providers[LOCAL].create(local_path1, BytesIO(b"hello"))
        found.append((REMOTE, remote_path1))

    cs.run_until_found(*found)
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)


@pytest.mark.repeat(4)
def test_sync_create_delete_same_name(cs):
    remote_parent = "/remote"
    local_parent = "/local"
    remote_path1 = "/remote/stuff1"
    local_path1 = "/local/stuff1"

    cs.providers[LOCAL].mkdir(local_parent)
    cs.providers[REMOTE].mkdir(remote_parent)

    linfo1 = cs.providers[LOCAL].create(local_path1, BytesIO(b"hello"))

    cs.run(until=lambda: not cs.state.has_changes(), timeout=2)

    rinfo = cs.providers[REMOTE].info_path(remote_path1)

    cs.emgrs[LOCAL].do()

    cs.providers[LOCAL].delete(linfo1.oid)

    cs.emgrs[LOCAL].do()

    linfo2 = cs.providers[LOCAL].create(local_path1, BytesIO(b"goodbye"))

    # run local event manager only... not sync
    cs.emgrs[LOCAL].do()

    log.info("TABLE 1\n%s", cs.state.pretty_print())
    # local and remote dirs can be disjoint

#    assert(len(cs.state) == 3 or len(cs.state) == 2)

    cs.run_until_found((REMOTE, remote_path1), timeout=2)

    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    log.info("TABLE 2\n%s", cs.state.pretty_print())

    # local and remote dirs can be disjoint
#    assert(len(cs.state) == 3 or len(cs.state) == 2)

    assert not cs.providers[LOCAL].info_path(local_path1 + ".conflicted")
    assert not cs.providers[REMOTE].info_path(remote_path1 + ".conflicted")

    rinfo = cs.providers[REMOTE].info_path(remote_path1)
    bio = BytesIO()
    cs.providers[REMOTE].download(rinfo.oid, bio)
    assert bio.getvalue() == b'goodbye'


# this test used to fail about 2 out of 10 times because of embracing a change that *wasn't properly indexed*
# it covers cases where events arrive in unexpected orders... could be possible to get the same coverage
# with a more deterministic version
@pytest.mark.repeat(10)
def test_sync_create_delete_same_name_heavy(cs):
    remote_parent = "/remote"
    local_parent = "/local"
    remote_path1 = "/remote/stuff1"
    local_path1 = "/local/stuff1"

    cs.providers[LOCAL].mkdir(local_parent)
    cs.providers[REMOTE].mkdir(remote_parent)

    import time, threading

    def creator():
        i = 0
        while i < 10:
            try:
                linfo1 = cs.providers[LOCAL].create(local_path1, BytesIO(b"file" + bytes(str(i),"utf8")))
                i += 1
            except CloudFileExistsError:
                linfo1 = cs.providers[LOCAL].info_path(local_path1)
                if linfo1:
                    cs.providers[LOCAL].delete(linfo1.oid)
            time.sleep(0.01)
    
    def done():
        bio = BytesIO()
        rinfo = cs.providers[REMOTE].info_path(remote_path1)
        if rinfo:
            cs.providers[REMOTE].download(rinfo.oid, bio)
            return bio.getvalue() == b'file' + bytes(str(9),"utf8")
        return False

    thread = threading.Thread(target=creator, daemon=True)
    thread.start()

    cs.run(until=done, timeout=3)

    thread.join()

    assert done()

    log.info("TABLE 2\n%s", cs.state.pretty_print())

    assert not cs.providers[LOCAL].info_path(local_path1 + ".conflicted")
    assert not cs.providers[REMOTE].info_path(remote_path1 + ".conflicted")

def test_sync_rename_heavy(cs):
    remote_parent = "/remote"
    local_parent = "/local"
    remote_sub = "/remote/sub"
    local_sub = "/local/sub"
    remote_path1 = "/remote/stuff1"
    local_path1 = "/local/stuff1"
    remote_path2 = "/remote/sub/stuff1"
    local_path2 = "/local/sub/stuff1"

    cs.providers[LOCAL].mkdir(local_parent)
    cs.providers[REMOTE].mkdir(remote_parent)
    cs.providers[LOCAL].mkdir(local_sub)
    cs.providers[REMOTE].mkdir(remote_sub)
    linfo1 = cs.providers[LOCAL].create(local_path1, BytesIO(b"file"))

    cs.do()
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    log.info("TABLE 1\n%s", cs.state.pretty_print())


    import time, threading

    oid = linfo1.oid
    done = False
    ok = True
    def mover():
        nonlocal done
        nonlocal oid
        nonlocal ok
        for _ in range(10):
            try:
                oid = cs.providers[LOCAL].rename(oid, local_path2)
                oid = cs.providers[LOCAL].rename(oid, local_path1)
                time.sleep(0.001)
            except Exception as e:
                log.exception(e)
                ok = False
        done = True

    thread = threading.Thread(target=mover, daemon=True)
    thread.start()

    cs.run(until=lambda: done, timeout=3)

    thread.join()

    log.info("TABLE 2\n%s", cs.state.pretty_print())

    cs.do()

    cs.run(until=lambda: not cs.state.has_changes(), timeout=1
            )
    log.info("TABLE 3\n%s", cs.state.pretty_print())

    assert ok
    assert cs.providers[REMOTE].info_path(remote_path1)

def test_sync_two_conflicts(cs):
    remote_path1 = "/remote/stuff1"
    local_path1 = "/local/stuff1"

    setup_remote_local(cs, "stuff1")

    log.info("TABLE 0\n%s", cs.state.pretty_print())

    linfo1 = cs.providers[LOCAL].info_path(local_path1)
    rinfo1 = cs.providers[REMOTE].info_path(remote_path1)

    cs.providers[LOCAL].delete(linfo1.oid)
    cs.providers[REMOTE].delete(rinfo1.oid)

    linfo2 = cs.providers[LOCAL].create(local_path1, BytesIO(b"goodbye"))
    linfo2 = cs.providers[REMOTE].create(remote_path1, BytesIO(b"world"))

    # run event managers only... not sync
    cs.emgrs[LOCAL].do()
    cs.emgrs[REMOTE].do()

    log.info("TABLE 1\n%s", cs.state.pretty_print())
    if cs.providers[LOCAL].oid_is_path:
        # the local delete/create doesn't add entries
        assert(len(cs.state) == 2)
    else:
        assert(len(cs.state) == 4)

    cs.run_until_found((REMOTE, remote_path1), timeout=2)

    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    # conflicted files are discarded, not in table
    log.info("TABLE 2\n%s", cs.state.pretty_print())
    assert(len(cs.state) == 2)

    assert cs.providers[LOCAL].info_path(local_path1 + ".conflicted") or cs.providers[REMOTE].info_path(remote_path1 + ".conflicted")

    b1 = BytesIO()
    b2 = BytesIO()

    cs.providers[LOCAL].download_path(local_path1, b1)
    cs.providers[LOCAL].download_path(local_path1 + ".conflicted", b2)

    assert b1.getvalue() in (b'goodbye', b'world')
    assert b2.getvalue() in (b'goodbye', b'world')
    assert b1.getvalue() != b2.getvalue()


@pytest.mark.repeat(10)
def test_sync_subdir_rename(cs):
    local_dir = "/local/a"
    local_base = "/local/a/stuff"
    local_dir2 = "/local/b"
    local_base2 = "/local/b/stuff"
    remote_dir = "/remote/a"
    remote_dir2 = "/remote/b"
    remote_base = "/remote/a/stuff"
    remote_base2 = "/remote/b/stuff"

    kid_count = 4
    cs.providers[LOCAL].mkdir("/local")

    lpoid = cs.providers[LOCAL].mkdir(local_dir)

    lpaths = []
    rpaths = []
    rpaths2 = []
    for i in range(kid_count):
        lpath = local_base + str(i)
        rpath = remote_base + str(i)
        rpath2 = remote_base2 + str(i)

        cs.providers[LOCAL].create(lpath, BytesIO(b'hello'))

        lpaths.append(lpath)
        rpaths.append((REMOTE, rpath))
        rpaths2.append((REMOTE, rpath2))

    cs.run_until_found(*rpaths, timeout=2)

    log.info("TABLE 1\n%s", cs.state.pretty_print())

    cs.providers[LOCAL].rename(lpoid, local_dir2)

    for _ in range(10):
        cs.do()

    log.info("TABLE 2\n%s", cs.state.pretty_print())

    cs.run_until_found(*rpaths2, timeout=2)

    log.info("TABLE 2\n%s", cs.state.pretty_print())

# this test is sensitive to the order in which things are processed
# so run it a few times


def test_sync_rename_over(cs):
    remote_parent = "/remote"
    local_parent = "/local"
    fn1 = "hello1"
    fn2 = "hello2"
    local_path1 = cs.providers[LOCAL].join(local_parent, fn1)  # "/local/hello1"
    local_path2 = cs.providers[LOCAL].join(local_parent, fn2)  # "/local/hello2"
    remote_path1 = cs.providers[REMOTE].join(remote_parent, fn1)  # "/remote/hello1"
    remote_path2 = cs.providers[REMOTE].join(remote_parent, fn2)  # "/remote/hello2"

    lpoid = cs.providers[LOCAL].mkdir(local_parent)
    linfo1 = cs.providers[LOCAL].create(local_path1, BytesIO(local_path1.encode('utf-8')))
    linfo2 = cs.providers[LOCAL].create(local_path2, BytesIO(local_path1.encode('utf-8')))

    cs.run_until_found((REMOTE, remote_path1), (REMOTE, remote_path2),  timeout=2)

    log.info("TABLE 1\n" + cs.state.pretty_print(use_sigs=False))
    # rename a file over another file by deleting the target and doing the rename in quick succession
    cs.providers[LOCAL].delete(linfo2.oid)
    cs.providers[LOCAL].rename(linfo1.oid, local_path2)

    log.info("TABLE 2\n" + cs.state.pretty_print(use_sigs=False))
    cs.run_until_found(WaitFor(side=REMOTE, path=remote_path1, exists=False),  timeout=2)
    log.info("TABLE 3\n%s", cs.state.pretty_print(use_sigs=False))

    # check the contents to make sure that path2 has path1's content
    new_oid = cs.providers[REMOTE].info_path(remote_path2).oid
    contents = BytesIO()
    cs.providers[REMOTE].download(new_oid, contents)
    assert contents.getvalue() == local_path1.encode('utf-8')

    # check that the folders each have only one file, and that it's path2
    rpoid = cs.providers[REMOTE].info_path(remote_parent).oid
    ldir = list(cs.providers[LOCAL].listdir(lpoid))
    rdir = list(cs.providers[REMOTE].listdir(rpoid))
    log.debug("ldir = %s", ldir)
    log.debug("rdir = %s", rdir)
    assert len(ldir) == 1
    assert ldir[0].path == local_path2
    assert len(rdir) == 1
    assert rdir[0].path == remote_path2


@pytest.mark.repeat(10)
def test_sync_folder_conflicts_file(cs):
    remote_path1 = "/remote/stuff1"
    remote_path2 = "/remote/stuff1/under"
    local_path1 = "/local/stuff1"

    setup_remote_local(cs, "stuff1")

    log.info("TABLE 0\n%s", cs.state.pretty_print())

    linfo1 = cs.providers[LOCAL].info_path(local_path1)
    rinfo1 = cs.providers[REMOTE].info_path(remote_path1)

    cs.providers[LOCAL].delete(linfo1.oid)
    cs.providers[REMOTE].delete(rinfo1.oid)

    linfo2 = cs.providers[LOCAL].create(local_path1, BytesIO(b"goodbye"))
    linfo2 = cs.providers[REMOTE].mkdir(remote_path1)
    linfo2 = cs.providers[REMOTE].create(remote_path2, BytesIO(b"world"))

    # run event managers only... not sync
    cs.emgrs[LOCAL].do()
    cs.emgrs[REMOTE].do()

    log.info("TABLE 1\n%s", cs.state.pretty_print())
    if cs.providers[LOCAL].oid_is_path:
        # there won't be 2 rows for /local/stuff1 is oid_is_path
        assert(len(cs.state) == 3)
        locs = cs.state.lookup_path(LOCAL, local_path1)
        assert locs and len(locs) == 1
        loc = locs[0]
        assert loc[LOCAL].otype == FILE
        assert loc[REMOTE].otype == DIRECTORY
    else:
        # deleted /local/stuff, remote/stuff, remote/stuff/under, lcoal/stuff, /local
        assert(len(cs.state) == 5)

    cs.run_until_found((REMOTE, remote_path1), timeout=2)

    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    log.info("TABLE 2\n%s", cs.state.pretty_print())
    assert(len(cs.state) == 4 or len(cs.state) == 3)

    local_conf = cs.providers[LOCAL].info_path(local_path1 + ".conflicted")
    remote_conf = cs.providers[REMOTE].info_path(remote_path1 + ".conflicted")

    assert local_conf and not remote_conf

    # file was moved out of the way for the folder
    assert local_conf.otype == FILE

    # folder won
    local_conf = cs.providers[LOCAL].info_path(local_path1)
    assert local_conf.otype == DIRECTORY


@pytest.fixture(params=[(MockStorage, dict()), (SqliteStorage, 'file::memory:?cache=shared')],
                ids=["mock_storage", "sqlite_storage"],
                name="storage"
                )
def storage_fixture(request):
    return request.param


def test_storage(storage):
    roots = ("/local", "/remote")
    storage_class = storage[0]
    storage_mechanism = storage[1]

    class CloudSyncMixin(CloudSync, RunUntilHelper):
        pass

    p1 = MockProvider(oid_is_path=False, case_sensitive=True)
    p2 = MockProvider(oid_is_path=False, case_sensitive=True)

    storage1: Storage = storage_class(storage_mechanism)
    cs1: CloudSync = CloudSyncMixin((p1, p2), roots, storage1, sleep=None)
    old_cursor = cs1.emgrs[0].state.storage_get_data(cs1.emgrs[0]._cursor_tag)
    assert old_cursor is not None
    log.debug("cursor=%s", old_cursor)

    test_sync_basic(cs1)  # do some syncing, to get some entries into the state table

    storage2 = storage_class(storage_mechanism)
    cs2: CloudSync = CloudSyncMixin((p1, p2), roots, storage2, sleep=None)

    log.debug(f"state1 = {cs1.state.entry_count()}\n{cs1.state.pretty_print()}")
    log.debug(f"state2 = {cs2.state.entry_count()}\n{cs2.state.pretty_print()}")

    def not_dirty(s: SyncState):
        for se in s.get_all():
            se: SyncEntry
            assert not se.dirty

    def compare_states(s1: SyncState, s2: SyncState) -> List[SyncEntry]:
        ret = []
        found = False
        for e1 in s1.get_all():
            e1: SyncEntry
            for e2 in s2.get_all():
                e2: SyncEntry
                if e1.serialize() == e2.serialize():
                    found = True
            if not found:
                ret.append(e1)
        return ret

    not_dirty(cs1.state)

    missing1 = compare_states(cs1.state, cs2.state)
    missing2 = compare_states(cs2.state, cs1.state)

    for e in missing1:
        log.debug(f"entry in 1 not found in 2 {e.pretty()}")
    for e in missing2:
        log.debug(f"entry in 2 not found in 1 {e.pretty()}")

    assert not missing1
    assert not missing2
    new_cursor = cs1.emgrs[0].state.storage_get_data(cs1.emgrs[0]._cursor_tag)
    log.debug("cursor=%s %s", old_cursor, new_cursor)
    assert new_cursor is not None
    assert old_cursor != new_cursor


@pytest.mark.parametrize("drain", [None, LOCAL, REMOTE])
def test_sync_already_there(cs, drain: int):
    local_parent = "/local"
    remote_parent = "/remote"
    remote_path1 = "/remote/stuff1"
    local_path1 = "/local/stuff1"

    cs.providers[LOCAL].mkdir(local_parent)
    cs.providers[REMOTE].mkdir(remote_parent)
    linfo1 = cs.providers[LOCAL].create(local_path1, BytesIO(b"hello"), None)
    rinfo2 = cs.providers[REMOTE].create(remote_path1, BytesIO(b"hello"), None)

    if drain is not None:
        # one of the event managers is not reporting events
        cs.emgrs[drain]._drain()

    # fill up the state table
    cs.do()

    # all changes processed
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    linfo1 = cs.providers[LOCAL].info_path(local_path1)
    rinfo1 = cs.providers[REMOTE].info_path(remote_path1)

    assert linfo1.hash == rinfo1.hash

    assert not cs.providers[LOCAL].info_path(local_path1 + ".conflicted")
    assert not cs.providers[REMOTE].info_path(remote_path1 + ".conflicted")


@pytest.mark.parametrize("drain", [LOCAL, REMOTE])
def test_sync_already_there_conflict(cs, drain: int):
    local_parent = "/local"
    remote_parent = "/remote"
    remote_path1 = "/remote/stuff1"
    local_path1 = "/local/stuff1"

    cs.providers[LOCAL].mkdir(local_parent)
    cs.providers[REMOTE].mkdir(remote_parent)
    cs.providers[LOCAL].create(local_path1, BytesIO(b"hello"), None)
    cs.providers[REMOTE].create(remote_path1, BytesIO(b"goodbye"), None)

    if drain is not None:
        # one of the event managers is not reporting events
        cs.emgrs[drain]._drain()

    # fill up the state table
    cs.do()

    # all changes processed
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    linfo1 = cs.providers[LOCAL].info_path(local_path1)
    rinfo1 = cs.providers[REMOTE].info_path(remote_path1)

    assert linfo1.hash == rinfo1.hash

    assert cs.providers[LOCAL].info_path(local_path1 + ".conflicted") or cs.providers[REMOTE].info_path(remote_path1 + ".conflicted")


def test_conflict_recover(cs):
    local_parent = "/local"
    remote_parent = "/remote"
    remote_path1 = "/remote/stuff1"
    local_path1 = "/local/stuff1"

    remote_path2 = "/remote/new_path"
    local_path2 = "/local/new_path"

    cs.providers[LOCAL].mkdir(local_parent)
    cs.providers[REMOTE].mkdir(remote_parent)
    cs.providers[LOCAL].create(local_path1, BytesIO(b"hello"), None)
    cs.providers[REMOTE].create(remote_path1, BytesIO(b"goodbye"), None)

    # fill up the state table
    cs.do()

    # all changes processed
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    linfo1 = cs.providers[LOCAL].info_path(local_path1)
    rinfo1 = cs.providers[REMOTE].info_path(remote_path1)

    assert linfo1.hash == rinfo1.hash

    local_conflicted_path = local_path1 + ".conflicted"
    remote_conflicted_path = remote_path1 + ".conflicted"
    local_conflicted = cs.providers[LOCAL].info_path(local_conflicted_path)
    remote_conflicted = cs.providers[REMOTE].info_path(remote_conflicted_path)

    log.info("CONFLICTED TABLE\n%s", cs.state.pretty_print())

    # Check that exactly one of the files is present
    assert bool(local_conflicted) or bool(remote_conflicted)
    assert bool(local_conflicted) != bool(remote_conflicted)

    log.info("BEFORE RENAME AWAY\n%s", cs.state.pretty_print())

    # Rename the conflicted file to something new
    if local_conflicted:
        cs.providers[LOCAL].rename(local_conflicted.oid, local_path2)
    else:
        cs.providers[REMOTE].rename(remote_conflicted.oid, remote_path2)

    # fill up the state table
    cs.do()

    # all changes processed
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    log.info("AFTER RENAME AWAY\n%s", cs.state.pretty_print())

    local_conflicted = cs.providers[LOCAL].info_path(local_conflicted_path)
    remote_conflicted = cs.providers[REMOTE].info_path(remote_conflicted_path)

    assert not bool(local_conflicted) and not bool(remote_conflicted)

    local_new = cs.providers[LOCAL].info_path(local_path2)
    remote_new = cs.providers[REMOTE].info_path(remote_path2)

    assert bool(local_new) and bool(remote_new)


def test_conflict_recover_modify(cs):
    local_parent = "/local"
    remote_parent = "/remote"
    remote_path1 = "/remote/stuff1"
    local_path1 = "/local/stuff1"

    remote_path2 = "/remote/new_path"
    local_path2 = "/local/new_path"

    # Create a clear-cut conflict
    cs.providers[LOCAL].mkdir(local_parent)
    cs.providers[REMOTE].mkdir(remote_parent)
    cs.providers[LOCAL].create(local_path1, BytesIO(b"hello"), None)
    cs.providers[REMOTE].create(remote_path1, BytesIO(b"goodbye"), None)

    cs.do()
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    linfo1 = cs.providers[LOCAL].info_path(local_path1)
    rinfo1 = cs.providers[REMOTE].info_path(remote_path1)
    assert linfo1.hash == rinfo1.hash

    local_conflicted_path = local_path1 + ".conflicted"
    remote_conflicted_path = remote_path1 + ".conflicted"
    local_conflicted = cs.providers[LOCAL].info_path(local_conflicted_path)
    remote_conflicted = cs.providers[REMOTE].info_path(remote_conflicted_path)

    log.info("CONFLICTED TABLE\n%s", cs.state.pretty_print())

    # Check that exactly one of the files is present
    assert bool(local_conflicted) or bool(remote_conflicted)
    assert bool(local_conflicted) != bool(remote_conflicted)

    if local_conflicted:
        assert local_conflicted.hash != linfo1.hash
        old_hash = local_conflicted.hash
    else:
        assert remote_conflicted.hash != rinfo1.hash
        old_hash = remote_conflicted.hash

    # Write some new content
    log.info("BEFORE MODIFY\n%s", cs.state.pretty_print())
    new_content = BytesIO(b"new content pls ignore")
    if local_conflicted:
        new_hash = cs.providers[LOCAL].upload(local_conflicted.oid, new_content).hash
    else:
        new_hash = cs.providers[REMOTE].upload(remote_conflicted.oid, new_content).hash

    assert new_hash != old_hash

    cs.do()
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    log.info("AFTER MODIFY\n%s", cs.state.pretty_print())
    local_conflicted = cs.providers[LOCAL].info_path(local_conflicted_path)
    remote_conflicted = cs.providers[REMOTE].info_path(remote_conflicted_path)
    assert bool(local_conflicted) or bool(remote_conflicted)
    assert bool(local_conflicted) != bool(remote_conflicted)

    # Rename the conflicted file to something new
    log.info("BEFORE RENAME AWAY\n%s", cs.state.pretty_print())

    if local_conflicted:
        cs.providers[LOCAL].rename(local_conflicted.oid, local_path2)
    else:
        cs.providers[REMOTE].rename(remote_conflicted.oid, remote_path2)

    cs.do()
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    log.info("AFTER RENAME AWAY\n%s", cs.state.pretty_print())
    local_conflicted = cs.providers[LOCAL].info_path(local_conflicted_path)
    remote_conflicted = cs.providers[REMOTE].info_path(remote_conflicted_path)
    assert not bool(local_conflicted) and not bool(remote_conflicted)

    # Check that the new path was uploaded
    local_new = cs.providers[LOCAL].info_path(local_path2)
    remote_new = cs.providers[REMOTE].info_path(remote_path2)
    assert bool(local_new) and bool(remote_new)
    assert local_new.hash == remote_new.hash

    # And now make sure that we're correctly processing new changes on the file
    newer_content = BytesIO(b"ok this is the last time fr")
    cs.providers[LOCAL].upload(local_new.oid, newer_content)

    cs.do()
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    local_newer = cs.providers[LOCAL].info_path(local_path2)
    remote_newer = cs.providers[REMOTE].info_path(remote_path2)
    assert bool(local_newer) and bool(remote_newer)
    assert local_newer.hash == remote_newer.hash


@pytest.mark.parametrize('right', (True, False), ids=["right_cs", "right_in"])
@pytest.mark.parametrize('left', (True, False), ids=["left_cs", "left_in"])
def test_sync_rename_folder_case(mock_provider_creator, left, right):
    cs = make_cs(mock_provider_creator, (True, left), (False, right))
    local_parent = "/local"
    remote_parent = "/remote"
    local_path1 = "/local/a"
    local_path2 = "/local/a/b"
    local_path3 = "/local/A"
    remote_path1 = "/remote/A"
    remote_path2 = "/remote/A/b"

    cs.providers[LOCAL].mkdir(local_parent)
    ldir = cs.providers[LOCAL].mkdir(local_path1)
    linfo = cs.providers[LOCAL].create(local_path2, BytesIO(b"hello"), None)

    cs.do()
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    log.debug("--- cs: %s ---", [e.case_sensitive for e in cs.providers])
    cs.providers[LOCAL].log_debug_state()
    cs.providers[REMOTE].log_debug_state()

    cs.providers[LOCAL].rename(ldir, local_path3)

    cs.do()
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    rinfo1 = cs.providers[REMOTE].info_path(remote_path1)
    rinfo2 = cs.providers[REMOTE].info_path(remote_path2)

    assert rinfo1 and rinfo2

    assert rinfo1.path == remote_path1
    assert rinfo2.path == remote_path2

# TODO: important tests: 
#    1. events coming in for path updates for conflicted files.... we should note conflict oids, and not insert them
#    2. for oid_as_path... events coming in for old creations, long since deleted or otherwise overwritten (renamed away, etc)


def test_sync_disconnect(cs):
    remote_parent = "/remote"
    local_parent = "/local"
    remote_path1 = "/remote/stuff1"
    local_path1 = "/local/stuff1"

    cs.providers[LOCAL].mkdir(local_parent)
    cs.providers[REMOTE].mkdir(remote_parent)

    linfo1 = cs.providers[LOCAL].create(local_path1, BytesIO(b"hello"))

    cs.providers[REMOTE].disconnect()

    assert not cs.providers[REMOTE].connected

    cs.run(until=lambda: cs.providers[REMOTE].connected, timeout=1)

    assert not cs.providers[REMOTE].info_path(remote_path1)

    cs.run_until_found((REMOTE, remote_path1))


def test_sync_rename_tmp(cs):
    remote_parent = "/remote"
    local_parent = "/local"
    remote_sub = "/remote/sub"
    local_sub = "/local/sub"
    remote_path1 = "/remote/stuff1"
    local_path1 = "/local/stuff1"
    remote_path2 = "/remote/sub/stuff1"
    local_path2 = "/local/sub/stuff1"

    cs.providers[LOCAL].mkdir(local_parent)
    cs.providers[REMOTE].mkdir(remote_parent)
    cs.providers[LOCAL].mkdir(local_sub)
    cs.providers[REMOTE].mkdir(remote_sub)

    cs.do()
    cs.run(until=lambda: not cs.state.has_changes(), timeout=1)

    log.info("TABLE 1\n%s", cs.state.pretty_print())


    import time, threading

    done = False
    ok = True
    def mover():
        nonlocal done
        nonlocal ok
        for _ in range(10):
            try:
                linfo1 = cs.providers[LOCAL].create(local_path1, BytesIO(b"file"))
                linfo2 = cs.providers[LOCAL].info_path(local_path2)
                if linfo2:
                    without_event = isinstance(cs.providers[LOCAL], MockProvider)
                    if without_event:
                        cs.providers[LOCAL]._delete(linfo2.oid, without_event=True)
                    else:
                        cs.providers[LOCAL].delete(linfo2.oid)
                cs.providers[LOCAL].rename(linfo1.oid, local_path2)
                time.sleep(0.001)
            except Exception as e:
                log.exception(e)
                ok = False
        done = True

    thread = threading.Thread(target=mover, daemon=True)
    thread.start()

    cs.run(until=lambda: done, timeout=3)

    thread.join()

    log.info("TABLE 2\n%s", cs.state.pretty_print())

    cs.do()

    cs.run(until=lambda: not cs.state.has_changes(), timeout=1
            )
    log.info("TABLE 3\n%s", cs.state.pretty_print())

    assert ok
    assert cs.providers[REMOTE].info_path(remote_path2)
    assert not cs.providers[REMOTE].info_path(remote_path2 + ".conflicted")
    assert not cs.providers[LOCAL].info_path(local_path2 + ".conflicted")
    assert not cs.providers[LOCAL].info_path(local_path1 + ".conflicted")
