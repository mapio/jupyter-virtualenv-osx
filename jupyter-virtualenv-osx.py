import argparse
import json
import os
import sys

from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory

def install_my_kernel_spec(name, user = True, prefix = None):
    kernel_json = {
        'argv': ['/usr/local/bin/python', '-m', 'echo_kernel', '-f', '{connection_file}'],
        'name': name,
        'env': { 'PYTHONHOME': os.environ['VIRTUAL_ENV'] },
        'language': 'python2',
    }
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        print('Installing Jupyter kernel spec')
        KernelSpecManager().install_kernel_spec(td, name, user = user, replace = True, prefix = prefix)

def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False

def main(argv = None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', help = 'The name of the installed kernel.', required = True)
    ap.add_argument('--user', action = 'store_true', help='Install to the per-user kernels registry. Default if not root.')
    ap.add_argument('--sys-prefix', action = 'store_true', help = 'Install to sys.prefix (e.g. a virtualenv or conda env)')
    ap.add_argument('--prefix', help = 'Install to the given prefix. Kernelspec will be installed in {PREFIX}/share/jupyter/kernels/')
    args = ap.parse_args(argv)

    if args.sys_prefix: args.prefix = sys.prefix
    if not args.prefix and not _is_root(): args.user = True

    install_my_kernel_spec(name = args.name, user = args.user, prefix = args.prefix)

if __name__ == '__main__':
    main()
