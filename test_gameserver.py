from attack import *
from EsseSubmitter import EsseSubmitter

target = Target("127.0.0.1", 5000)


@local
@once
@attack(target)
@submit(EsseSubmitter)
def test_gameserver(target: Target):
    return "NOT_A_FLAG"
