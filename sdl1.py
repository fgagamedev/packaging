from datetime import date
import os
import shutil
import string
import subprocess as sp
import sys


class Repository:

    def __init__(self, url, branch='master', name=None):
        self.project = {
            'project_name': 'Ankh',
            'lib_name': 'Ankh_lib',
            'release_date': date.today(),
            'src_folder': 'src',
        }

        args = ['rm', '-rf', 'repo/']
        sp.call(args)

        args = ['git', 'clone', url, 'repo', '-b', branch]
        sp.call(args)

        if name is None:
            name = url.split('/')[-1]
            name = name.split('.')[0]
            name = name.lower()

        self.project['project_name'] = name.replace('-', '_')

        self.project['lib_name'] = self.project['project_name'].split('_')
        if len(self.project['lib_name']) > 1:
            self.project['lib_name'] = self.project['lib_name'][0]
        else:
            self.project['lib_name'] = self.project['lib_name'][0] + '_lib'

        self.project['src_folder'] = 'src' if 'src' in os.listdir('repo') else 'source'


    def find_media(self):
        os.chdir('repo')

        dirs = os.listdir()
        if 'resources' in dirs:
            self.project['media_dir'] = 'resources'
        elif 'res' in dirs:
            self.project['media_dir'] = 'res'
        elif 'media' in dirs:
            self.project['media_dir'] = 'media'
        elif 'sounds' in dirs:
            self.project['media_dir'] = 'sounds'
        elif 'data' in dirs:
            self.project['media_dir'] = 'data'

        os.chdir('..')

    def build(self):
        os.chdir('repo')
        sp.call('./linux/build.sh')
        sp.call(['./linux/create_installer.sh', 'all'])

    def rename(self):
        rename = (
            'repo/linux/project_name',
            'repo/dist/linux/packages/project_name',
        )

        for name in rename:
            new_name = name.replace('project_name', self.project['project_name'])
            shutil.move(name, new_name)

    def copy_files(self):
        # 'repo/dist/linux/packages/project_name/meta/license.txt' #copy license from root (COPY LICENSE!!!)
        shutil.copy2('templates_sdl1/CMakeLists.txt.root', 'repo/CMakeLists.txt')
        shutil.copy2('templates_sdl1/CMakeLists.txt.src',
                     'repo/'+ self.project['src_folder'] + '/CMakeLists.txt')

        root_folders = [
            'lib',
            'Qt',
            'dist',
            'linux',
        ]

        os.chdir('repo')
        sp.call(['rm', '-rf'] + root_folders)
        os.chdir('..')
        # print(os.listdir())

        for folder in root_folders:
            shutil.copytree('templates_sdl1/'+ folder, 'repo/' + folder)

    def find_source(self):
        os.chdir('repo/' + self.project['src_folder'])

        tmp_files = os.walk('.')
        src_files = ''
        for root, subfolders, files in tmp_files:
            root += '/' # Add a final slash
            root = root[2:] # Remove './' if it exists
            for f in files:
                if f.find('.c') > 0:
                    src_files = src_files + root + f + ' '

        self.project['source_files'] = src_files
        os.chdir('../..')

    def replace_info(self):
        files = (
            'repo/CMakeLists.txt',
            'repo/' + self.project['src_folder'] + '/CMakeLists.txt',
            'repo/dist/linux/config/config.xml',
            'repo/dist/linux/packages/project_name/meta/launcher.qs',
            'repo/dist/linux/packages/project_name/meta/package.xml',
            'repo/linux/build.sh',
            'repo/linux/create_installer.sh',
            'repo/linux/project_name',
            'repo/linux/run.sh',
        )

        for f in files:
            print('==============', f)
            self.replace(f)

    def replace(self, file_name):
        with open(file_name, 'r') as f:
            text = f.read()

        with open(file_name, 'w') as f:
            text = string.Template(text)
            f.write(text.safe_substitute(**self.project))


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 3:
        rep = Repository(url=args[1], branch=args[2])
    elif len(args) == 2:
        rep = Repository(url=args[1])
    else:
        raise TypeError('You must pass the repository url!!')
    rep.copy_files()
    rep.find_media()
    rep.find_source()
    rep.replace_info()
    rep.rename()
    rep.build()
