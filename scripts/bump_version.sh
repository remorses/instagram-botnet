set -ex
cd `dirname $0`
cd ../src

version=`cat VERSION`

bumpversion --current-version $version minor ./VERSION
