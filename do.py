#! /usr/bin/env python3

#===== imports =====#
import argparse
import datetime
import os
import re
import signal
import subprocess
import sys

#===== args =====#
parser = argparse.ArgumentParser()
parser.add_argument('--gpu-info', action='store_true')
parser.add_argument('--gpu-monitor', action='store_true')
parser.add_argument('--build', '-b', action='store_true')
parser.add_argument('--image-bash', action='store_true')
parser.add_argument('--image-gpu-info', action='store_true')
parser.add_argument('--image-check-cuda', action='store_true')
parser.add_argument('--run', '-r', action='store_true')
parser.add_argument('--bash', action='store_true')
args = parser.parse_args()

#===== consts =====#
DIR = os.path.dirname(os.path.realpath(__file__))

#===== setup =====#
os.chdir(DIR)

#===== helpers =====#
def blue(text):
    return '\x1b[34m' + text + '\x1b[0m'

def timestamp():
    return '{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())

def invoke(
    *args,
    quiet=False,
    env_add={},
    handle_sigint=True,
    popen=False,
    check=True,
    out=False,
    err=False,
    **kwargs,
):
    if len(args) == 1 and type(args[0]) == str:
        args = args[0].split()
    if not quiet:
        print(blue('-'*40))
        print(timestamp())
        print(os.getcwd()+'$', end=' ')
        if any([re.search(r'\s', i) for i in args]):
            print()
            for i in args: print(f'\t{i} \\')
        else:
            for i, v in enumerate(args):
                if i != len(args)-1:
                    end = ' '
                else:
                    end = ';\n'
                print(v, end=end)
        if kwargs: print(kwargs)
        if popen: print('popen')
        print()
    if env_add:
        env = os.environ.copy()
        env.update(env_add)
        kwargs['env'] = env
    if out or err: kwargs['capture_output'] = True
    p = subprocess.Popen(args, **kwargs)
    if handle_sigint:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    if popen:
        return p
    p.wait()
    if handle_sigint:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    if check and p.returncode:
        raise Exception(f'invocation {repr(args)} returned code {p.returncode}.')
    if out:
        stdout = p.stdout.decode('utf-8')
        if out != 'exact': stdout = stdout.strip()
        if not err: return stdout
    if err:
        stderr = p.stderr.decode('utf-8')
        if err != 'exact': stderr = stderr.strip()
        if not out: return stderr
    if out and err: return [stdout, stderr]
    return p

#===== main =====#
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

if args.gpu_info:
    print('===== hardware =====')
    invoke('sudo lshw -c display')
    print()
    print('===== driver =====')
    invoke('nvidia-smi')

if args.gpu_monitor:
    invoke('nvtop')

if args.build:
    invoke('docker build -t stable-diffusion-webui .')

if args.image_bash:
    invoke('''docker run
        --gpus all
        -it
        --rm
        stable-diffusion-webui
        bash
    ''')

if args.image_gpu_info:
    print('===== hardware =====')
    invoke('docker', 'run',
        '--gpus', 'all',
        '--user', 'root',
        '--rm',
        'stable-diffusion-webui',
        'bash', '-c', 'apt update && apt install -y lshw && lshw -c display',
    )
    print()
    print('===== driver =====')
    invoke('''docker run
        --gpus all
        --rm
        stable-diffusion-webui
        nvidia-smi
    ''')

if args.image_check_cuda:
    python_cmd = '; '.join([
        'import torch',
        'print("CUDA version:", torch.version.cuda)',
        'print("CUDA available:", torch.cuda.is_available())',
        'assert torch.cuda.is_available()',
    ])
    invoke('docker', 'run',
        '--gpus', 'all',
        '--rm',
        'stable-diffusion-webui',
        'bash', '-c', f"source venv/bin/activate; python3 -c '{python_cmd}'",
    )

if args.run:
    invoke('mkdir -p models')
    invoke('mkdir -p outputs')
    uid = os.getuid()
    invoke(f'sudo chown 10000:{uid} -R models outputs')
    invoke('sudo chmod 775 -R models outputs')
    if os.path.exists('run_extra_webui_args.txt'):
        with open('run_extra_webui_args.txt') as f:
            extra_webui_args = f.read()
    else:
        extra_webui_args = ''
    invoke(f'''docker run
        --name stable-diffusion-webui
        --gpus all
        --network host
        -v {DIR}/models:/app/stable-diffusion-webui/models
        -v {DIR}/outputs:/app/stable-diffusion-webui/outputs
        -d
        stable-diffusion-webui
        bash webui.sh --listen {extra_webui_args}
    ''')
    invoke('cp model.pt models/model.pt')

if args.bash:
    invoke('docker exec -it stable-diffusion-webui bash')
