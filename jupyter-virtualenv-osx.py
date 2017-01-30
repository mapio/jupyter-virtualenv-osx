from argparse import ArgumentParser
from json import dump
import os
import sys
from tempfile import mkdtemp
from shutil import rmtree

from jupyter_client.kernelspec import KernelSpecManager

def install_my_kernel_spec(name, user = True, prefix = None):
    kernel_json = {
        'argv': ['/usr/local/bin/python', '-m', 'ipykernel', '-f', '{connection_file}'],
        'name': name,
        'env': {'PYTHONHOME': os.environ.get('VIRTUAL_ENV', '')},
        'language': 'python2',
    }
    tempdir = mkdtemp()
    with open(os.path.join(tempdir, 'kernel.json'), 'w') as f:
        dump(kernel_json, f, sort_keys=True)
    print('Installing Jupyter kernel spec')
    KernelSpecManager().install_kernel_spec(tempdir , name, user = user, replace = True, prefix = prefix)
    rmtree(tempdir)

def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False

def main():
    ap = ArgumentParser()
    ap.add_argument('--name', help = 'The name of the installed kernel.', required = True)
    ap.add_argument('--user', action = 'store_true', help='Install to the per-user kernels registry. Default if not root.')
    ap.add_argument('--sys-prefix', action = 'store_true', help = 'Install to sys.prefix (e.g. a virtualenv or conda env)')
    ap.add_argument('--prefix', help = 'Install to the given prefix. Kernelspec will be installed in {PREFIX}/share/jupyter/kernels/')
    args = ap.parse_args()

    if args.sys_prefix: args.prefix = sys.prefix
    if not args.prefix and not _is_root(): args.user = True

    install_my_kernel_spec(name = args.name, user = args.user, prefix = args.prefix)

if __name__ == '__main__':
    main()
