from module.step.common_step import CommonStep


def test(fc_name):
    import module.test.core_tester
    cls = module.test.core_tester.TestScreen()
    fc = getattr(cls, fc_name)
    res = fc()
    return res


def restart():
    CommonStep.ensureGameOpenAndInMain()
