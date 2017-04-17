"""Package a sgfmill release.

Requires a release_sgfmill.conf file, eg:

«
# All paths are relative to this config file
repo_dir = "."
working_dir = "./tmp/release"
log_pathname = "./tmp/release/release.log"
target_dir = "./tmp/release"
html_files_to_remove = [
    ".buildinfo",
]
»

"""

import os
import re
import shutil
import sys
from optparse import OptionParser
from subprocess import check_call, check_output, CalledProcessError, Popen, PIPE

class Failure(Exception):
    pass

def read_python_file(pathname):
    dummy = {}
    result = {}
    with open(pathname, 'rb') as f:
        bb = f.read()
    exec(bb, dummy, result)
    return result

def is_safe_tag(s):
    if s in (".", ".."):
        return False
    return bool(re.search(r"\A[-_.a-zA-Z0-9]+\Z", s))

def is_acceptable_version(s):
    if s in (".", ".."):
        return False
    if len(s) > 12:
        return False
    return bool(re.search(r"\A[-_.a-zA-Z0-9]+\Z", s))

def export_tag(dst, repo_dir, tag):
    """Export from the git tag.

    repo_dir -- git repository to export from (must contain .git)
    tag      -- tag to export
    dst      -- directory to export into

    The exported tree will be placed in a directory named <tag> inside <dst>.

    All files have the timestamp of the commit referred to by the tag.

    """
    if not os.path.isdir(os.path.join(repo_dir, ".git")):
        raise Failure("No .git repo in %s" % repo_dir)
    try:
        check_call("git archive --remote=%s --prefix=%s/ %s | tar -C %s -xf -" %
                   (repo_dir, tag, tag, dst),
                   shell=True)
    except CalledProcessError:
        raise Failure("export failed")

def prepare_dir():
    """Make any required changes in the exported distribution directory.

    cwd must be the distribution directory (the project root).

    """
    os.rename("README.sdist.txt", "README.txt")
    os.remove("README.rst")

def get_version():
    """Obtain the sgfmill version from setup.py."""
    try:
        output = check_output("python setup.py --version".split(),
                              universal_newlines=True)
    except CalledProcessError:
        raise Failure("'setup.py --version' failed")
    version = output.strip()
    if not is_acceptable_version(version):
        raise Failure("bad version: %s" % repr(version))
    return version

def make_sdist(version, logfile):
    """Run 'setup.py sdist'.

    cwd must be the distribution directory (the project root).

    Returns the pathname of the sdist tar.gz, relative to the distribution
    directory.

    """
    try:
        check_call("python setup.py sdist".split(), stdout=logfile)
    except CalledProcessError:
        raise Failure("'setup.py sdist' failed")
    result = os.path.join("dist", "sgfmill-%s.tar.gz" % version)
    if not os.path.exists(result):
        raise Failure("'setup.py sdist' did not create %s" % result)
    return result

def make_wheel(version, logfile):
    """Run 'setup.py bdist_wheel'.

    cwd must be the distribution directory (the project root).

    Returns the pathname of the sdist tar.gz, relative to the distribution
    directory.

    """
    try:
        check_call("python setup.py bdist_wheel".split(), stdout=logfile)
    except CalledProcessError:
        raise Failure("'setup.py bdist_wheel' failed")
    result = os.path.join("dist", "sgfmill-%s-py3-none-any.whl" % version)
    if not os.path.exists(result):
        raise Failure("'setup.py bdist_wheel' did not create %s" % result)
    return result

def make_sphinx(version, logfile, html_files_to_remove):
    """Run build_docs and make a tarball.

    cwd must be the distribution directory (the project root).

    Returns the pathname of the docs tar.gz, relative to the distribution
    directory.

    """
    try:
        check_call(["./build_docs"], stdout=logfile)
    except CalledProcessError:
        raise Failure("'build_docs' failed")
    htmlpath = os.path.join("doc", "_build", "html")
    for filename in html_files_to_remove:
        os.remove(os.path.join(htmlpath, filename))
    os.rename(htmlpath, "sgfmill-doc-%s" % version)
    try:
        check_call(("tar -czf sgfmill-doc-%s.tar.gz sgfmill-doc-%s" %
                    (version, version)).split())
    except CalledProcessError:
        raise Failure("tarring up sgfmill-doc failed")
    return "sgfmill-doc-%s.tar.gz" % version

def do_release(tag, config_pathname):
    config_dir = os.path.abspath(os.path.dirname(config_pathname))
    os.chdir(config_dir)

    try:
        config = read_python_file(config_pathname)
    except Exception as e:
        raise Failure("error reading config file:\n%s" % e)

    export_dir = os.path.join(config['working_dir'], tag)
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)
    export_tag(config['working_dir'], config['repo_dir'], tag)
    logfile = open(config['log_pathname'], "w")
    os.chdir(export_dir)
    prepare_dir()
    version = get_version()
    sdist_pathname = make_sdist(version, logfile)
    wheel_pathname = make_wheel(version, logfile)
    docs_pathname = make_sphinx(version, logfile,
                                config['html_files_to_remove'])
    os.chdir(config_dir)
    logfile.close()
    sdist_dst = os.path.join(config['target_dir'],
                             os.path.basename(sdist_pathname))
    wheel_dst = os.path.join(config['target_dir'],
                             os.path.basename(wheel_pathname))
    docs_dst = os.path.join(config['target_dir'],
                            os.path.basename(docs_pathname))
    if os.path.exists(sdist_dst):
        os.remove(sdist_dst)
    if os.path.exists(wheel_dst):
        os.remove(wheel_dst)
    if os.path.exists(docs_dst):
        os.remove(docs_dst)
    shutil.move(os.path.join(export_dir, sdist_pathname), sdist_dst)
    shutil.move(os.path.join(export_dir, wheel_pathname), wheel_dst)
    shutil.move(os.path.join(export_dir, docs_pathname), docs_dst)
    shutil.rmtree(export_dir)


USAGE = """\
%(prog)s <tag>\
"""

def main(argv):
    parser = OptionParser(usage=USAGE)
    opts, args = parser.parse_args(argv)
    if len(args) != 1:
        parser.error("wrong number of arguments")
    tag = args[0]
    if not is_safe_tag(tag):
        parser.error("ill-formed tag")
    config_pathname = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "release_sgfmill.conf")
    try:
        if not os.path.exists(config_pathname):
            raise Failure("config file %s does not exist" % config_pathname)
        do_release(tag, config_pathname)
    except (OSError, Failure) as e:
        print("release_sgfmill.py: %s" % e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
