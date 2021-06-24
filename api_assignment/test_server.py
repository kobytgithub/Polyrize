from api.api_actions import ApiActions
from deepdiff import DeepDiff
import conftest


def test_authenticate():
    args = conftest.get_args()
    username = None
    password = None
    expect_to_fail = False
    if "username" in args:
        username = args["username"]
    if "password" in args:
        password = args["password"]
    if "expect_to_fail" in args:
        expect_to_fail = args["expect_to_fail"]
    api = ApiActions()
    authentication = api.authenticate(username, password)
    if expect_to_fail:
        assert not authentication
    else:
        assert authentication


def test_get_object_list():
    api = ApiActions()
    api.authenticate()
    object_list = api.get_object_list()
    assert object_list


def test_get_object_by_id():
    args = conftest.get_args()
    expect_to_fail = False
    api = ApiActions()
    api.authenticate()
    if "expect_to_fail" in args:
        expect_to_fail = args["expect_to_fail"]
    if "object_id" in args:
        object_id = args["object_id"]
    else:
        object_list = api.get_object_list()
        object_id = object_list[0]["object_id"]
    obj = api.get_object(obj_id=object_id)
    if expect_to_fail:
        assert not obj
    else:
        assert obj


def test_create_object():
    args = conftest.get_args()
    api = ApiActions()
    api.authenticate()
    dict_obj = None
    if "dict_obj" in args:
        dict_obj = args["dict_obj"]
    obj = api.create_object(dict_obj=dict_obj)
    assert obj


def test_delete_object():
    args = conftest.get_args()
    api = ApiActions()
    api.authenticate()
    if "object_id" in args:
        object_id = args["object_id"]
    else:
        created_obj = api.create_object()
        object_id = created_obj["id"]
    object_list = api.get_object_list()
    found = False
    for obj in object_list:
        if obj["object_id"] == object_id:
            found = True
            break
    if found:
        print(f"Object id [{object_id}] was found, created successfully")
    else:
        print(f"Object id [{object_id}] was not found, Failed to create object")
        assert found
    deleted = api.delete_object(obj_id=object_id)
    if not deleted:
        assert deleted
    object_list = api.get_object_list()
    found = False
    for obj in object_list:
        if obj["object_id"] == object_id:
            found = True
            break
    if found:
        print(f"Object id [{object_id}] was found, Failed to delete object")
    else:
        print(f"Object id [{object_id}] was not found, deleted successfully")
    assert not found


def test_create_object_and_verify():
    args = conftest.get_args()
    api = ApiActions()
    api.authenticate()
    dict_obj = None
    if "dict_obj" in args:
        dict_obj = args["dict_obj"]
    created_obj = api.create_object(dict_obj=dict_obj)
    obj_id = created_obj["id"]
    verify_created_obj = api.get_object(obj_id=obj_id)
    verify_created_obj_data = verify_created_obj["data"]
    diff = DeepDiff(dict_obj["data"], verify_created_obj_data, ignore_order=True)
    if diff:
        print(f"Failed, there is a difference between the created object and the object we got from the server, diff: [{diff}]")
    else:
        print("Both objects are equal")
    assert not diff
