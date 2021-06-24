from scenario import ScenarioParser
import pytest

current_test_number = -1
pytest.args = []
pytest.current_test_id = -1


def pytest_runtest_setup(item):
    global current_test_number
    current_test_number = current_test_number + 1
    pytest.current_test_id += 1


def pytest_collection_modifyitems(items):
    scenario = ScenarioParser()
    test_list = scenario.get_test_list()
    temp_items = items[:]
    del items[:]

    for test_node in test_list:
        for test in temp_items:
            if test.name == test_node['test']:
                items.append(test)
                pytest.args.append(test_node)


def get_args():
    return pytest.args[pytest.current_test_id]
