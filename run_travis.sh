#!/bin/bash

tox -epep8
retval=$?
tox -ecover
exit $retval