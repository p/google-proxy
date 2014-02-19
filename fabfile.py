from fabric.api import *
import time, os.path, os

env.shell = '$SHELL -c'

env.app = 'gp'
env.repo_url = os.path.abspath(os.path.dirname(__file__))
env.user = 'bpa'
env.hosts = ['localhost']
base = '/home/%s/%s' % (env.user, env.app)
env.repo_path = os.path.join(base, 'repo')
env.webroot_path = os.path.join(base, 'webroot')

def chain_commands(commands):
    chained = ' && '.join(cmd.strip() for cmd in commands)
    return chained

def setup():
    cmd = chain_commands([
        'git init %s' % env.repo_path,
        'cd %s' % env.repo_path,
        'git remote add upstream %s' % env.repo_url,
        'mkdir -p %s' % env.webroot_path,
    ])
    run(cmd)

def reset():
    run('rm -rf %s' % env.repo_path)

def deploy():
    cmd = chain_commands([
        'cd %s' % env.repo_path,
        'git fetch upstream',
        'git reset --hard upstream/master',
        'rsync -a --delete --exclude .git %s/ %s' % (env.repo_path, env.webroot_path),
        'cd %s' % env.webroot_path,
        'ln -s %s' % '/home/pie/apps/webracer/webracer',
        'ln -s %s' % '/home/pie/apps/ocookie/ocookie',
        'ln -s %s' % '/home/pie/apps/cidict/cidict.py',
    ])
    run(cmd)

def find_binary(name):
    for dir in os.environ['PATH'].split(':'):
        path = os.path.join(dir, name)
        # will return path to scripts that are not executable
        if os.path.exists(path):
            return path
    raise ValueError('%s not found in PATH' % name)

def restart():
    cmd = chain_commands([
        '(pkill python || true)',
        '%s /home/bpa/gp/webroot/fastcgi.py' % find_binary('python'),
    ])
    run(cmd)
