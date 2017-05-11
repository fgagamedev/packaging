from datetime import date
import os
import shutil
import string
import subprocess as sp
import sys


class Repository:

    def __init__(self, url, branch='master', name=None):
        os.chdir('..')
        self.project = {
            'project_name': 'Ankh',
            'lib_name': 'Ankh_lib',
            'release_date': date.today()
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

    def find_media(self):
        os.chdir('repo')

        dirs = os.listdir()
        if 'resources' in dirs:
            self.project['media_dir'] = 'resources'
        elif 'res' in dirs:
            self.project['media_dir'] = 'res'
        elif 'media' in dirs:
            self.project['media_dir'] = 'media'

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
        shutil.copy2('templates/CMakeLists.txt.root', 'repo/CMakeLists.txt')
        shutil.copy2('templates/CMakeLists.txt.src', 'repo/src/CMakeLists.txt')

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
            shutil.copytree('templates/'+ folder, 'repo/' + folder)

    def find_source(self):
        tmp_files = os.listdir('repo/src')
        src_files = ''
        for src in tmp_files:
            if src.find('.c') > 0:
                src_files = src_files + src + ' '

        self.project['source_files'] = src_files

    def replace_info(self):
        files = (
            'repo/CMakeLists.txt',
            'repo/src/CMakeLists.txt',
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
    rep = Repository(url=args[1], branch=args[2])
    rep.copy_files()
    rep.find_media()
    rep.find_source()
    rep.replace_info()
    rep.rename()
    rep.build()
