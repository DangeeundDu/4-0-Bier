import time

from attack_targets import Target
from typing import Callable, Union
from enum import Enum
from abc import abstractmethod
from threading import Timer
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from sys import float_info


def flatten(l):
    return list(chain(l))


class Reason(Enum):
    OWN_FLAG = 0
    EXPIRED_FLAG = 1
    WRONG_FLAG = 2
    REPEATED_FLAG = 3


class AttackLogger:
    @abstractmethod
    def log(msg: str):
        pass

    @abstractmethod
    def log_success_flags(self, count: int, message: str = ""):
        pass

    @abstractmethod
    def log_bad_flags(self, count: int, reason: Reason, message: str = ""):
        pass


class NoFlag:
    reason: Reason

    def __init__(self, reason):
        self.reason = reason


SubmittableFlags = list[Union[str, NoFlag]]


class Submitter:
    logger: AttackLogger

    def log(self):
        return self.logger

    @abstractmethod
    def __call__(self, flags: SubmittableFlags):
        pass


def tautology(_):
    return True


class AttackMethode:
    targets: list[Target] = None
    attack_function: Callable[[Target], Union[str, list[str]]] = None
    interval_seconds: int = 1
    logger: AttackLogger = None
    submitter: Submitter = None
    max_threads: int = 0
    seconds_to_start: int = 0
    stop_time: float = float_info.max
    attacks_left: int = -1
    predicate = tautology

    def start(self):
        if self.submitter and self.logger:
            self.submitter.logger = self.logger

        if not self.targets or not self.attack_function:
            print("You have to specify at least one target and an attack function")
            exit(1)

        def execute_attack():
            if self.attacks_left == 0 or self.stop_time < time.time() or not self.predicate():
                return
            elif self.attacks_left > 0:
                self.attacks_left -= 1

            if len(self.targets) == 1 or self.max_threads == 1:
                try:
                    with self.targets[0] as attack_target:
                        flags = self.attack_function(attack_target)
                        if type(flags) is list:
                            self.submitter(flags)
                        else:
                            self.submitter([flags])
                except:
                    pass

                Timer(self.interval_seconds, execute_attack).start()
            else:

                def enter_target(_target: Target):
                    try:
                        with _target as t:
                            flags = self.attack_function(t)
                            if type(flags) is list:
                                self.submitter(flags)
                            else:
                                self.submitter([flags])
                    except:
                        pass  # If one service is down, we will get errors connecting to it. This should however not
                        # stop
                        # us from attacking the other services

                with ThreadPoolExecutor(max_workers=self.max_threads) as exe:
                    results = exe.map(enter_target, self.targets, chunksize=1)
                    self.submitter(flatten(results))

                Timer(self.interval_seconds, execute_attack).start()

        if self.seconds_to_start == 0:
            execute_attack()
        else:
            Timer(self.seconds_to_start, execute_attack).start()


def submit(submitter: type):
    if not issubclass(submitter, Submitter):
        print("Please provide a valid submitter")
        exit(1)

    def __inner(f: Union[AttackMethode, Callable[[Union[Target, list[Target]]], str], str]):
        if type(f) is AttackMethode:
            f.submitter = submitter()
            return f
        elif callable(f):
            attack_methode = AttackMethode()
            attack_methode.submitter = submitter()
            attack_methode.attack_function = f
            return attack_methode

        print("Please either provide an attack methode function or structure")
        exit(1)

    return __inner


def attack(target: Union[Target, list[Target]]):
    targets: list[Target]
    if type(target) is not list:
        targets = [target]

    def __inner(f: Union[AttackMethode, Callable[[Union[Target, list[Target]]], str], str]):
        if type(f) is AttackMethode:
            f.targets = targets
            return f
        elif callable(f):
            attack_methode = AttackMethode()
            attack_methode.attack_function = f
            attack_methode.targets = targets
            return attack_methode

        print("Please either provide an attack methode function or structure")
        exit(1)

    return __inner


def log(logger: type):
    if not issubclass(logger, Submitter):
        print("Please provide a valid submitter")
        exit(1)

    def __inner(f: Union[AttackMethode, Callable[[Union[Target, list[Target]]], str], str]):
        if type(f) is AttackMethode:
            f.logger = logger()
            return f
        elif callable(f):
            attack_methode = AttackMethode()
            attack_methode.logger = logger()
            attack_methode.attack_function = f
            return attack_methode

        print("Please either provide an attack methode function or structure")
        exit(1)

    return __inner


def at(hours, minutes, seconds):
    if hours < 0 or hours > 23 or minutes < 0 or minutes > 60 or seconds < 0 or seconds > 60:
        print("Please input a valid time!")
        exit(-1)

    def __inner(f: Union[AttackMethode, Callable[[Union[Target, list[Target]]], str], str]):
        local_time = time.localtime()
        start_time = time.mktime(
            time.strptime(
                f"{local_time.tm_mday} {local_time.tm_mon:02} {local_time.tm_year} {hours}:{minutes}:{seconds}",
                "%d %m %Y %H:%M:%S"))

        wait = start_time - time.time()
        if wait < 0:
            print("Please input a time in the future")
            exit(1)

        if type(f) is AttackMethode:
            f.seconds_to_start = wait
            return f
        elif callable(f):
            attack_methode = AttackMethode()
            attack_methode.attack_function = f
            attack_methode.seconds_to_start = wait
            return attack_methode

        print("Please either provide an attack methode function or structure")
        exit(1)

    return __inner


def once(f: Union[AttackMethode, Callable[[Union[Target, list[Target]]], str], str]):
    if type(f) is AttackMethode:
        f.attacks_left = 1
        return f
    elif callable(f):
        attack_methode = AttackMethode()
        attack_methode.attack_function = f
        attack_methode.attacks_left = 1
        return attack_methode

    print("Please either provide an attack methode function or structure")
    exit(1)


def repeat(times: int):
    def __inner(f: Union[AttackMethode, Callable[[Union[Target, list[Target]]], str], str]):
        current_time = time.localtime()
        if type(f) is AttackMethode:
            f.attacks_left = times
            return f
        elif callable(f):
            attack_methode = AttackMethode()
            attack_methode.attack_function = f
            attack_methode.attacks_left = times
            return attack_methode

        print("Please either provide an attack methode function or structure")
        exit(1)

    return __inner


def after(seconds=5, minutes=0, hours=0):
    def __inner(f: Union[AttackMethode, Callable[[Union[Target, list[Target]]], str], str]):
        if type(f) is AttackMethode:
            f.seconds_to_start = seconds + minutes * 60 + hours * 3600
            return f
        elif callable(f):
            attack_methode = AttackMethode()
            attack_methode.attack_function = f
            attack_methode.seconds_to_start = seconds + minutes * 6 + hours * 36000
            return attack_methode

        print("Please either provide an attack methode function or structure")
        exit(1)

    return __inner


def every(seconds=5, minutes=0, hours=0):
    def __inner(f):
        if type(f) is AttackMethode:
            f.interval_seconds = seconds + minutes * 60 + hours * 3600
            return f
        elif callable(f):
            attack_methode = AttackMethode()
            attack_methode.attack_function = f
            attack_methode.interval_seconds = seconds + minutes * 6 + hours * 36000
            return attack_methode

    return __inner


def do_for(hours: int, minutes: int, seconds: int):
    def __inner(f: Union[AttackMethode, Callable[[Union[Target, list[Target]]], str], str]):
        current_time = time.time()
        if type(f) is AttackMethode:
            f.stop_time = current_time + hours * 3600 + minutes * 60 + seconds
            return f
        elif callable(f):
            attack_methode = AttackMethode()
            attack_methode.attack_function = f
            attack_methode.stop_time = current_time + hours * 3600 + minutes * 60 + seconds
            return attack_methode

        print("Please either provide an attack methode function or structure")
        exit(1)

    return __inner


def until(hours: int, minutes: int, seconds: int = 0):
    def __inner(f: Union[AttackMethode, Callable[[Union[Target, list[Target]]], str], str]):
        local_time = time.localtime()
        stop_time = time.mktime(
            time.strptime(
                f"{local_time.tm_mday} {local_time.tm_mon:02} {local_time.tm_year} {hours}:{minutes}:{seconds}",
                "%d %m %Y %H:%M:%S"))

        if type(f) is AttackMethode:
            f.stop_time = stop_time
            return f
        elif callable(f):
            attack_methode = AttackMethode()
            attack_methode.attack_function = f
            attack_methode.stop_time = stop_time
            return attack_methode

        print("Please either provide an attack methode function or structure")
        exit(1)

    return __inner


def do_while(predicate: Callable[[], bool]):
    def __inner(f: Union[AttackMethode, Callable[[Union[Target, list[Target]]], str], str]):
        if type(f) is AttackMethode:
            f.predicate = predicate
            return f
        elif callable(f):
            attack_methode = AttackMethode()
            attack_methode.attack_function = f
            attack_methode.predicate = predicate
            return attack_methode

        print("Please either provide an attack methode function or structure")
        exit(1)

    return __inner


def local(f: AttackMethode):
    f.start()
