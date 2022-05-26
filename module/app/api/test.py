from flask import Blueprint, jsonify, request
from flask_login import login_required
import module.schedule.otherScheduler
import module.test.core_tester
from logzero import logger

app_test = Blueprint("app_test", __name__)


# 获取状态
@app_test.route('/test', methods=['get'])
@login_required
def test():
    fc_name = request.args.get("fc")
    if fc_name is None:
        return jsonify({'result': "error function fc=None"})
    cls = module.test.core_tester.TestScreen()
    try:
        getattr(cls, fc_name)
        res = module.schedule.otherScheduler.test(fc_name)
        return jsonify({'result': "please wait for result"})
    except AttributeError as e:
        logger.warning(e)
        return jsonify({'result': "error function fc={}".format(fc_name)})


# 获取状态
@app_test.route('/testlist', methods=['get'])
@login_required
def testlist():
    import inspect
    from module.test.core_tester import TestScreen
    lis = inspect.getmembers(TestScreen, inspect.isfunction)
    res = []
    for t in lis:
        if "test_" in t[0]:
            fc_name = t[0]
            fc_desc = t[1].__annotations__.get("desc")
            res.append([fc_name, fc_desc])
    return jsonify({'result': res})
