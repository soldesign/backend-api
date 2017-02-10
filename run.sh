#!/usr/bin/env bash

# get to the path of the script
pushd `dirname $0` > /dev/null
scriptpath=`pwd`
popd > /dev/null
cd $scriptpath


echo "================================================================================"
echo "=============== preparation: install needed packages in a virtualenv ==========="
echo "================================================================================"

# if venv does not exist create it
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# source the venv
. venv/bin/activate

# (re-)install the needed packages
pip3 install pip wheel --upgrade

pip3 install -r requirements.txt

echo "================================================================================"
echo "=============== preparation done: starting application ========================="
echo "================================================================================"


hug -f run.py
