set -ex

cd `dirname $0`
cd ../src

bumpversion --current-version version minor VERSION

git add VERSION
git commit -m "version $version"
git tag -a "$version" -m "version $version"
git config credential.helper 'cache --timeout=120'
git config user.email $GITHUBUSERNAME
git config user.name $GITHUBPASSWORD
git push
