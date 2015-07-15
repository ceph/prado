#!/usr/bin/env python

import os
import sys
import shutil
import tarfile

markupsafe="https://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-0.23.tar.gz#md5=f5ab3deee4c37cd6a922fb81e730da6e"
jinja2="https://pypi.python.org/packages/source/J/Jinja2/Jinja2-2.7.3.tar.gz#md5=b9dffd2f3b43d673802fe857c8445b1a"
ansible="https://pypi.python.org/packages/source/a/ansible/ansible-1.9.1.tar.gz#md5=3c0f0ecc8b5d60831b10045dba64bbbb"
pyyaml="https://pypi.python.org/packages/source/P/PyYAML/PyYAML-3.11.tar.gz#md5=f50e08ef0fe55178479d3a618efe21db"
six="https://pypi.python.org/packages/source/s/six/six-1.9.0.tar.gz#md5=476881ef4012262dfc8adc645ee786c4"

cwd = os.path.abspath(os.path.dirname(__file__))
top_level_dir = os.path.dirname(cwd)
build_dir = os.path.join(top_level_dir, 'build')
sources_dir = os.path.join(build_dir, 'sources')
rebuild = sys.argv[-1] in ['--rebuild', '--force', 'rebuild', 'force']


def log(string):
    print '--> %s' % string


def mkdir(path, endpart=None):
    if endpart:
        path = os.path.join(path, endpart)
    if not os.path.exists(path):
        log('creating directory: %s' % path)
        os.mkdir(path)
    else:
        log('path already exists, not re-creating: %s' % path)


def rmdir(path, endpart=None):
    if endpart:
        path = os.path.join(path, endpart)
    if os.path.exists(path):
        log('removing directory: %s' % path)
        try:
            shutil.rmtree(path)
        except OSError as err:
            log('WARN: %s' % err)
    else:
        log('path does not exist: %s' % path)


def wget(url, save_as):
    if not rebuild:
        return
    import urllib2
    response = urllib2.urlopen(url)
    with open(save_as, 'w') as _file:
        _file.write(response.read())


def cp(source, destination):
    log('copying from %s to %s' % (source, destination))
    if os.path.isfile(source):
        shutil.copyfile(source, destination)
        return
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def setup():
    """
    Remove old build stuff except for the sources
    """
    if rebuild:
        rmdir(build_dir)
    mkdir(build_dir)
    mkdir(sources_dir)
    rmdir(build_dir, 'bin')
    rmdir(build_dir, 'ansible')


def tar_xzf(path, destination=sources_dir):
    tar = tarfile.open(path)
    directory_name = os.path.commonprefix(tar.getnames())
    extracted_path = os.path.join(destination, directory_name)
    tar.extractall(destination)
    tar.close()
    return extracted_path


def setup_ansible():
    log('*'*40+' setting up ansible ' + '*'*40)
    save_as = os.path.join(sources_dir, 'ansible.tar.gz')
    wget(ansible, save_as)
    extracted_path = tar_xzf(save_as)
    # copy the whole thing because this is the base for everything ansible
    destination = os.path.join(build_dir, 'ansible')
    cp(extracted_path, destination)


def setup_markupsafe():
    log('*'*40+' setting up markupsafe ' + '*'*40)
    save_as = os.path.join(sources_dir, 'markupsafe.tar.gz')
    wget(markupsafe, save_as)
    extracted_path = tar_xzf(save_as)
    library_path = os.path.join(extracted_path, 'markupsafe')
    destination = os.path.join(build_dir, 'ansible/lib/markupsafe')
    cp(library_path, destination)


def setup_jinja2():
    log('*'*40+' setting up jinja2 ' + '*'*40)
    save_as = os.path.join(sources_dir, 'jinja2.tar.gz')
    wget(jinja2, save_as)
    extracted_path = tar_xzf(save_as)
    library_path = os.path.join(extracted_path, 'jinja2')
    destination = os.path.join(build_dir, 'ansible/lib/jinja2')
    cp(library_path, destination)


def setup_pyyaml():
    log('*'*40+' setting up pyyaml ' + '*'*40)
    save_as = os.path.join(sources_dir, 'pyyaml.tar.gz')
    wget(pyyaml, save_as)
    extracted_path = tar_xzf(save_as)
    library_path = os.path.join(extracted_path, 'lib/yaml')
    destination = os.path.join(build_dir, 'ansible/lib/yaml')
    cp(library_path, destination)


def setup_six():
    log('*'*40+' setting up six ' + '*'*40)
    save_as = os.path.join(sources_dir, 'six.tar.gz')
    wget(six, save_as)
    extracted_path = tar_xzf(save_as)
    library_path = os.path.join(extracted_path, 'six.py')
    destination = os.path.join(build_dir, 'ansible/lib/six.py')
    cp(library_path, destination)


def main():
    log('setting up build...')
    setup()
    setup_ansible()
    setup_markupsafe()
    setup_jinja2()
    setup_pyyaml()
    setup_six()
    cp(
        os.path.join(top_level_dir, 'bin'),
        os.path.join(build_dir, 'bin')
    )


if __name__ == '__main__':
    main()
