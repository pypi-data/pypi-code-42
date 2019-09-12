"""Queue class for interacting with the queue.

File format versions:

5) Changed from mod:func to mod@func.
6) Relative paths.

"""
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Set, List, Dict, Optional, Sequence  # noqa
from types import TracebackType

from .config import config
from .scheduler import get_scheduler, Scheduler
from .resources import Resources
from .run import run_tasks
from .task import Task
from .utils import Lock
from .virtenv import find_activation_scripts

use_color = sys.stdout.isatty()


class Selection:
    """Object used for selecting tasks."""

    def __init__(self,
                 ids: Optional[Set[int]] = None,
                 name: str = '',
                 states: Set[str] = set(),
                 folders: List[Path] = [],
                 recursive: bool = True):
        """Selection.

        Selections is based on:

            ids

        or:

            any combination of name, state, folder.

        Use recursive=True to allow for tasks inside a folder.
        """
        self.ids = ids
        self.name = name
        self.states = states
        self.folders = folders
        self.recursive = recursive

    def __repr__(self) -> str:
        return (f'Selection({self.ids}, {self.name}, {self.states}, '
                f'{self.folders}, {self.recursive})')


class Queue(Lock):
    """Object for interacting with the scheduler."""
    def __init__(self,
                 verbosity: int = 1,
                 need_lock: bool = True,
                 dry_run: bool = False):
        self.verbosity = verbosity
        self.need_lock = need_lock
        self.dry_run = dry_run

        self.folder = config['home'] / '.myqueue'
        self.fname = self.folder / 'queue.json'

        Lock.__init__(self, self.fname.with_name('queue.json.lock'))

        self._scheduler: Optional[Scheduler] = None
        self.tasks: List[Task] = []
        self.changed = False

    @property
    def scheduler(self) -> Scheduler:
        """Scheduler object."""
        if self._scheduler is None:
            schedulername = config.get('scheduler',
                                       config.get('queue'))
            if schedulername is None:
                home = config['home']
                raise ValueError(
                    'Please specify type of scheduler in your '
                    f'{home}/.myqueue/config.py '
                    "file (must be 'slurm', 'pbs' or 'local').  See "
                    'https://myqueue.rtfd.io/en/latest/configuration.html')
            self._scheduler = get_scheduler(schedulername)
        return self._scheduler

    def __enter__(self) -> 'Queue':
        if self.dry_run:
            return self
        if self.need_lock:
            self.acquire()
        else:
            try:
                self.acquire()
            except PermissionError:
                pass
        return self

    def __exit__(self,
                 type: Exception,
                 value: Exception,
                 tb: TracebackType) -> None:
        if self.changed:
            assert not self.dry_run
            self._write()
        self.release()

    def list(self,
             selection: Selection,
             columns: str,
             sort: str = None,
             reverse: bool = False,
             short: bool = False) -> List[Task]:
        """Pretty-print list of tasks."""
        self._read()
        tasks = self.select(selection)
        if isinstance(sort, str):
            tasks.sort(key=lambda task: task.order(sort),  # type: ignore
                       reverse=reverse)
        pprint(tasks, self.verbosity, columns, short)
        return tasks

    def info(self, id: int) -> None:
        """Print information about a single task."""
        self._read()
        task = self.select(Selection({id}, '', set(), [], False))[0]
        print(json.dumps(task.todict(), indent='    '))
        if self.verbosity > 1:
            path = task.folder / (task.name + '.err')
            try:
                err = path.read_text()
            except FileNotFoundError:
                pass
            else:
                try:
                    N = os.get_terminal_size().columns - 1
                except OSError:
                    N = 70
                print(f'\nError file: {path}')
                print('v' * N)
                print(err)
                print('^' * N)

    def submit(self,
               tasks: Sequence[Task],
               read: bool = True) -> None:
        """Submit tasks to queue."""
        tasks2 = []
        done = set()
        for task in tasks:
            if task.workflow and task.is_done():
                done.add(task.dname)
            else:
                tasks2.append(task)
        tasks = tasks2

        if done:
            print(plural(len(done), 'task'), 'already done')

        tasks = [task
                 for task in tasks
                 if not task.workflow or not task.has_failed()]
        nfailed = len(tasks2) - len(tasks)
        if nfailed:
            print(plural(nfailed, 'task'),
                  'already marked as FAILED '
                  '("<task-name>.FAILED" file exists)')

        if read:
            self._read()

        current = {task.dname: task for task in self.tasks}

        tasks2 = []
        inqueue: Dict[str, int] = defaultdict(int)
        for task in tasks:
            if task.workflow and task.dname in current:
                inqueue[current[task.dname].state] += 1
                task.id = current[task.dname].id
            else:
                tasks2.append(task)
        tasks = tasks2

        if inqueue:
            print(plural(sum(inqueue.values()), 'task'),
                  'already in the queue:')
            print('\n'.join('    {:8}: {}'.format(state, n)
                            for state, n in inqueue.items()))

        todo = []
        for task in tasks:
            task.dtasks = []
            for dep in task.deps:
                # convert dep to Task:
                tsk = current.get(dep)
                if tsk is None:
                    for tsk in tasks:
                        if dep == tsk.dname:
                            break
                    else:
                        if dep not in done:
                            print('Missing dependency:', dep)
                            break
                        tsk = None
                elif tsk.state == 'done':
                    tsk = None
                elif tsk.state not in ['queued', 'hold', 'running']:
                    print('Dependency ({}) in bad state: {}'
                          .format(tsk.name, tsk.state))
                    break

                if tsk is not None:
                    task.dtasks.append(tsk)
            else:
                task.deps = [t.dname for t in task.dtasks]
                todo.append(task)

        # All dependensies must have an id or be in the list of tasks
        # about to be submitted
        n1 = len(todo)
        while True:
            todo = [task for task in todo
                    if all(tsk.id or tsk in todo
                           for tsk in task.dtasks)]
            n2 = len(todo)
            if n2 == n1:
                break
            n1 = n2

        t = time.time()
        for task in todo:
            task.dtasks = [tsk for tsk in task.dtasks if not tsk.is_done()]
            task.state = 'queued'
            task.tqueued = t

        if self.dry_run:
            pprint(todo, 0, 'fnr')
            print(plural(len(todo), 'task'), 'to submit')
        else:
            activation_scripts = find_activation_scripts([task.folder
                                                          for task in todo])
            submitted = []
            ex = None
            while todo:
                task = todo.pop(0)
                if not all(t.id != 0 for t in task.dtasks):
                    # dependency has not been submitted yet
                    todo.append(task)
                else:
                    try:
                        self.scheduler.submit(
                            task,
                            activation_scripts.get(task.folder))
                    except Exception as x:
                        ex = x
                        break
                    else:
                        submitted.append(task)

            pprint(submitted, 0, 'ifnr')
            if submitted:
                print(plural(len(submitted), 'task'), 'submitted')

            self.tasks += submitted
            self.changed = True
            self.scheduler.kick()

            if ex:
                print('ERROR:', task)
                print(task, task.todict(), ex, todo, file=sys.stderr)
                raise ex

    def run(self,
            tasks: List[Task]) -> None:
        """Run tasks locally."""
        self._read()
        dnames = {task.dname for task in tasks}
        self._remove([task for task in self.tasks if task.dname in dnames])
        if self.dry_run:
            for task in tasks:
                print(f'{task.folder}: {task.cmd}')
        else:
            run_tasks(tasks)

    def select(self, s: Selection) -> List[Task]:
        """Filter tasks acording to selection object."""
        if s.ids is not None:
            return [task for task in self.tasks if task.id in s.ids]

        tasks = []
        for task in self.tasks:
            if task.state in s.states:
                if not s.name or task.cmd.name == s.name:
                    if any(task.infolder(f, s.recursive) for f in s.folders):
                        tasks.append(task)

        return tasks

    def remove(self, selection: Selection) -> None:
        """Remove or cancel tasks."""

        self._read()

        tasks = self.select(selection)
        tasks = self.find_depending(tasks)

        self._remove(tasks)

    def _remove(self, tasks: List[Task]) -> None:
        t = time.time()
        for task in tasks:
            if task.tstop is None:
                task.tstop = t  # XXX is this for dry_run only?

        if self.dry_run:
            pprint(tasks, 0)
            print(plural(len(tasks), 'task'), 'to be removed')
        else:
            if self.verbosity > 0:
                pprint(tasks, 0)
                print(plural(len(tasks), 'task'), 'removed')
            for task in tasks:
                if task.state in ['running', 'hold', 'queued']:
                    self.scheduler.cancel(task)
                self.tasks.remove(task)
                # XXX why cancel?
                task.cancel_dependents(self.tasks, time.time())
            self.changed = True

    def sync(self) -> None:
        """Syncronize queue with the real world."""
        self._read()
        in_the_queue = ['running', 'hold', 'queued']
        ids = self.scheduler.get_ids()
        remove = []
        for task in self.tasks:
            if task.state in in_the_queue and task.id not in ids:
                remove.append(task)
            elif not task.folder.is_dir():
                remove.append(task)

        if remove:
            if self.dry_run:
                print(plural(len(remove), 'job'), 'to be removed')
            else:
                for task in remove:
                    self.tasks.remove(task)
                self.changed = True
                print(plural(len(remove), 'job'), 'removed')

    def find_depending(self, tasks: List[Task]) -> List[Task]:
        """Generate list of tasks including dependencies."""
        map = {task.dname: task for task in self.tasks}
        d: Dict[Task, List[Task]] = defaultdict(list)
        for task in self.tasks:
            for dname in task.deps:
                tsk = map.get(dname)
                if tsk:
                    d[tsk].append(task)

        removed = []

        def remove(task: Task) -> None:
            removed.append(task)
            for j in d[task]:
                remove(j)

        for task in tasks:
            remove(task)

        return sorted(set(removed), key=lambda task: task.id)

    def modify(self,
               selection: Selection,
               newstate: str) -> None:
        """Modify task(s)."""
        self._read()
        tasks = self.select(selection)

        for task in tasks:
            if task.state == 'hold' and newstate == 'queued':
                if self.dry_run:
                    print('Release:', task)
                else:
                    self.scheduler.release_hold(task)
            elif task.state == 'queued' and newstate == 'hold':
                if self.dry_run:
                    print('Hold:', task)
                else:
                    self.scheduler.hold(task)
            elif task.state == 'FAILED' and newstate in ['MEMORY', 'TIMEOUT']:
                if self.dry_run:
                    print('FAILED ->', newstate, task)
                else:
                    task.remove_failed_file()
            else:
                raise ValueError('Can\'t do {} -> {}!'
                                 .format(task.state, newstate))
            print('{} -> {}: {}'.format(task.state, newstate, task))
            task.state = newstate
            self.changed = True

    def resubmit(self,
                 selection: Selection,
                 resources: Optional[Resources]) -> None:
        """Resubmit failed or timed-out tasks."""
        self._read()
        tasks = []
        for task in self.select(selection):
            if not self.dry_run:
                if task.state not in {'queued', 'hold', 'running'}:
                    self.tasks.remove(task)
                if task.state == 'FAILED':
                    task.remove_failed_file()
            task = Task(task.cmd,
                        deps=task.deps,
                        resources=resources or task.resources,
                        folder=task.folder,
                        workflow=task.workflow,
                        restart=task.restart,
                        creates=task.creates,
                        diskspace=0)
            tasks.append(task)
        self.submit(tasks, read=False)

    def _read(self) -> None:
        if self.fname.is_file():
            data = json.loads(self.fname.read_text())
            root = self.folder.parent
            for dct in data['tasks']:
                task = Task.fromdict(dct, root)
                self.tasks.append(task)

        if self.locked:
            self.read_change_files()
            self.check()

    def read_change_files(self) -> None:
        paths = list(self.folder.glob('*-*-*'))
        files = []
        for path in paths:
            _, id, state = path.name.split('-')
            files.append((path.stat().st_ctime, int(id), state))
        states = {'0': 'running',
                  '1': 'done',
                  '2': 'FAILED',
                  '3': 'TIMEOUT'}
        for t, id, state in sorted(files):
            self.update(id, states[state], t)

        if files:
            self.changed = True

        for path in paths:
            path.unlink()

    def update(self,
               id: int,
               state: str,
               t: float = 0.0) -> None:

        for task in self.tasks:
            if task.id == id:
                break
        else:
            print('No such task: {id}, {state}'
                  .format(id=id, state=state))
            return

        t = t or time.time()

        task.state = state

        if state == 'done':
            for tsk in self.tasks:
                if task.dname in tsk.deps:
                    tsk.deps.remove(task.dname)
            task.write_done_file()
            task.tstop = t

        elif state == 'running':
            task.trunning = t

        elif state in ['FAILED', 'TIMEOUT', 'MEMORY']:
            task.cancel_dependents(self.tasks, t)
            task.tstop = t
            if state == 'FAILED':
                task.write_failed_file()

        else:
            raise ValueError('Bad state: ' + state)

        self.changed = True

    def check(self) -> None:
        t = time.time()

        for task in self.tasks:
            if task.state == 'running':
                delta = t - task.trunning - task.resources.tmax
                if delta > 0:
                    if self.scheduler.timeout(task) or delta > 1800:
                        task.state = 'TIMEOUT'
                        task.tstop = t
                        task.cancel_dependents(self.tasks, t)
                        self.changed = True

        bad = {task.dname for task in self.tasks if task.state.isupper()}
        for task in self.tasks:
            if task.state == 'queued':
                for dep in task.deps:
                    if dep in bad:
                        task.state = 'CANCELED'
                        task.tstop = t
                        self.changed = True
                        break

        for task in self.tasks:
            if task.state == 'FAILED':
                if not task.error:
                    oom = task.read_error()
                    if oom:
                        task.state = 'MEMORY'
                        task.remove_failed_file()
                    self.changed = True

    def kick(self) -> int:
        """Restart timed-out and out-of-memory tasks."""
        self._read()
        tasks = []
        for task in self.tasks:
            if task.state in ['TIMEOUT', 'MEMORY'] and task.restart:
                nodes = config.get('nodes') or [('', {'cores': 1})]
                if not self.dry_run:
                    task.resources.double(task.state, nodes)
                    task.restart -= 1
                tasks.append(task)
        if tasks:
            tasks = self.find_depending(tasks)
            if self.dry_run:
                pprint(tasks)
            else:
                print('Restarting', plural(len(tasks), 'task'))
                for task in tasks:
                    self.tasks.remove(task)
                    task.error = ''
                    task.id = 0
                self.submit(tasks, read=False)

        self.hold_or_release()

        return len(tasks)

    def hold_or_release(self) -> None:
        maxmem = config.get('maximum_diskspace', float('inf'))
        mem = 0
        for task in self.tasks:
            if task.state in {'queued', 'running'}:
                mem += task.diskspace

        if mem > maxmem:
            for task in self.tasks:
                if task.state == 'queued':
                    if task.diskspace > 0:
                        self.scheduler.hold(task)
                        task.state = 'hold'
                        self.changed = True
                        mem -= task.diskspace
                        if mem < maxmem:
                            break
        elif mem < maxmem:
            for task in self.tasks[::-1]:
                if task.state == 'hold' and task.diskspace > 0:
                    self.scheduler.release_hold(task)
                    task.state = 'queued'
                    self.changed = True
                    mem += task.diskspace
                    if mem > maxmem:
                        break

    def _write(self) -> None:
        root = self.folder.parent
        text = json.dumps(
            {'version': 6,
             'warning': 'Do NOT edit this file!',
             'unless': 'you know what you are doing.',
             'tasks': [task.todict(root)
                       for task in self.tasks]},
            indent=2)
        self.fname.write_text(text)


def plural(n: int, thing: str) -> str:
    if n == 1:
        return '1 ' + thing
    return '{} {}s'.format(n, thing)


def colored(state: str) -> str:
    if state.isupper():
        return '\033[91m' + state + '\033[0m'
    if state.startswith('done'):
        return '\033[92m' + state + '\033[0m'
    return state


def pprint(tasks: List[Task],
           verbosity: int = 1,
           columns: str = 'ifnraste',
           short: bool = False) -> None:

    if verbosity < 0:
        return

    if not tasks:
        return

    home = str(Path.home()) + '/'
    cwd = str(Path.cwd()) + '/'

    titles = ['id', 'folder', 'name', 'res.', 'age', 'state', 'time', 'error']
    c2i = {title[0]: i for i, title in enumerate(titles)}
    indices = [c2i[c] for c in columns]

    if verbosity:
        lines = [[titles[i] for i in indices]]
        lengths = [len(t) for t in lines[0]]
    else:
        lines = []
        lengths = [0] * len(columns)

    count: Dict[str, int] = defaultdict(int)
    for task in tasks:
        words = task.words()
        _, folder, _, _, _, state, _, _ = words
        count[state] += 1
        if folder.startswith(cwd):
            words[1] = './' + folder[len(cwd):]
        elif folder.startswith(home):
            words[1] = '~/' + folder[len(home):]
        words = [words[i] for i in indices]
        lines.append(words)
        lengths = [max(n, len(word)) for n, word in zip(lengths, words)]

    try:
        N = os.get_terminal_size().columns
        cut = max(0, N - sum(L + 1 for L, c in zip(lengths, columns)
                             if c != 'e'))
    except OSError:
        cut = 999999

    if verbosity:
        lines[1:1] = [['-' * L for L in lengths]]
        lines.append(lines[1])

    if not short:
        for words in lines:
            words2 = []
            for word, c, L in zip(words, columns, lengths):
                if c == 'e':
                    word = word[:cut]
                elif c in 'at':
                    word = word.rjust(L)
                else:
                    word = word.ljust(L)
                    if c == 's' and use_color:
                        word = colored(word)
                words2.append(word)
            print(' '.join(words2))

    if verbosity:
        count['total'] = len(tasks)
        print(', '.join('{}: {}'.format(state, n)
                        for state, n in count.items()))
