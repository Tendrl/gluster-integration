import ctypes
import importlib
from mock import MagicMock
from mock import patch


@patch.object(ctypes, "CDLL")
@patch.object(ctypes, "CFUNCTYPE")
def test_glusterlibgfapiexception(cdll, cfunc):
    cfunc.return_value = MagicMock()
    cdll.return_value = MagicMock()
    gfapi = importlib.import_module("tendrl.gluster_integration.gfapi")
    gfapi.find_library = MagicMock()
    result = str(gfapi.GlusterLibgfapiException())
    if result != "Gluster Libgfapi Exception":
        raise AssertionError


@patch.object(ctypes, "CDLL")
@patch.object(ctypes, "CFUNCTYPE")
def test_glfsstatvfsexception(cdll, cfunc):
    cfunc.return_value = MagicMock()
    cdll.return_value = MagicMock()
    gfapi = importlib.import_module("tendrl.gluster_integration.gfapi")
    gfapi.find_library = MagicMock()
    result = str(gfapi.GlfsStatvfsException())
    if result != "Failed to get Gluster volume Size info":
        raise AssertionError


@patch.object(ctypes, "CDLL")
@patch.object(ctypes, "CFUNCTYPE")
def test_glfsinitexception(cdll, cfunc):
    cfunc.return_value = MagicMock()
    cdll.return_value = MagicMock()
    gfapi = importlib.import_module("tendrl.gluster_integration.gfapi")
    gfapi.find_library = MagicMock()
    result = str(gfapi.GlfsInitException())
    if result != "glfs init failed":
        raise AssertionError


@patch.object(ctypes, "CDLL")
@patch.object(ctypes, "CFUNCTYPE")
def test_glfsfiniexception(cdll, cfunc):
    cfunc.return_value = MagicMock()
    cdll.return_value = MagicMock()
    gfapi = importlib.import_module("tendrl.gluster_integration.gfapi")
    gfapi.find_library = MagicMock()
    result = str(gfapi.GlfsFiniException())
    if result != "glfs fini failed":
        raise AssertionError
