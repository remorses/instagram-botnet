set -ex
cd `dirname $0`
cd ../src

test -f ./VERSION || (echo "file VERSION containing current version is needed" && exit 1)

python3 setup.py sdist bdist_wheel

python3 -m twine upload -u $PYPIUSERNAME -p $PYPIPASSWORD  dist/*
