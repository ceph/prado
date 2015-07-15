#!/bin/bash
set -e
set -x

markupsafe="https://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-0.23.tar.gz#md5=f5ab3deee4c37cd6a922fb81e730da6e"
jinja2="https://pypi.python.org/packages/source/J/Jinja2/Jinja2-2.7.3.tar.gz#md5=b9dffd2f3b43d673802fe857c8445b1a"
ansible="https://pypi.python.org/packages/source/a/ansible/ansible-1.9.1.tar.gz#md5=3c0f0ecc8b5d60831b10045dba64bbbb"
pyyaml="https://pypi.python.org/packages/source/P/PyYAML/PyYAML-3.11.tar.gz#md5=f50e08ef0fe55178479d3a618efe21db"
six="https://pypi.python.org/packages/source/s/six/six-1.9.0.tar.gz#md5=476881ef4012262dfc8adc645ee786c4"

fetch=$1

get_source() {
    mkdir -p $2
    cd $2
    if [ ! -z  "$fetch" ]
        then
            wget $1
            tar xzf *tar.gz
            rm -f *tar.gz
    fi
}

cwd=`dirname $0`

# create the build dir, remove everything before hand, always
build_dir="$cwd/../build"
echo $build_dir
echo $cwd

if [ ! -z  "$fetch" ]
    then
        rm -rf "$build_dir/bin"
        rm -rf "$build_dir/ansible"
fi
sources_dir="$build_dir/sources"
mkdir -p "$build_dir"
mkdir -p "$sources_dir"

cd "$sources_dir"


# start with ansible because it includes the 'lib' dir
get_source $ansible ansible
cp -r ansible* $build_dir/ansible

## MarkupSafe
#cd "$sources_dir"
#get_source $markupsafe markupsafe
#cp -r MarkupSafe*/markupsafe "$build_dir/ansible/lib/"
#
## jinja2
#cd "$sources_dir"
#get_source $jinja2 jinja2
#cp -r Jinja2*/jinja2 "$build_dir/ansible/lib/"
#
## pyyaml
#cd "$sources_dir"
#get_source $pyyaml pyyaml
#cp -r PyYAML*/lib/yaml "$build_dir/ansible/lib/"
#
#
## six
#cd "$sources_dir"
#get_source $six six
#cp -r six*/six.py "$build_dir/ansible/lib/"
#
## Now copy the bin files
#cd "$sources_dir"
#cp -r "$build_dir/../bin" "$build_dir"
#
#echo "Testing to see if the build worked..."
#$build_dir/bin/ansible --version
#rc=$?
#if [[ $rc != 0 ]]
#  then
#    echo "something went wrong with the build. Ansible script returned with error code: $rc"
#else
#    echo "All good. Build is good to go"
#fi
