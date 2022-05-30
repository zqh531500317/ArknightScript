from module.step.common_step import CommonStep
from module.base import my_annotation, before


def test(fc_name):
    import module.test.core_tester
    cls = module.test.core_tester.TestScreen()
    fc = getattr(cls, fc_name)
    res = fc()
    return res


@before
@my_annotation(desc="重启")
def restart():
    CommonStep.ensureGameOpenAndInMain()
