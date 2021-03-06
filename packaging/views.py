from datetime import date
import os
import shutil
import string
import subprocess as sp

import requests

from rest_framework import viewsets
from rest_framework.response import Response


class PackageViewSet(viewsets.ViewSet):
    project = {
        'project_name': 'Ankh',
        'lib_name': 'Ankh_lib',
        'release_date': date.today()
    }

    def clone(self, request, *args, **kwargs):
        args = ['rm', '-rfv', 'repo/']
        sp.call(args)

        url = request.data['url']
        try:
            branch = request.data['branch']
        except:
            branch = 'master'
        args = ['git', 'clone', url, 'repo', '-b', branch]

        sp.call(args)
        self.project['url'] = url

        try:
            name = request.data['name']
        except:
            name = request.data['url'].split('/')[-1]
            name = name.split('.')[0]
            name = name.lower()

        self.project['project_name'] = name

        self.project['lib_name'] = self.project['project_name'].split('-')
        if len(self.project['lib_name']) > 1:
            self.project['lib_name'] = self.project['lib_name'][0]
        else:
            self.project['lib_name'] = self.project['lib_name'][0] + '_lib'

        return Response()

    def make(self, request, *args, **kwargs):
        self.copy_files()
        self.find_media()
        self.find_source()
        self.replace_info()
        self.rename()
        self.build()

        return Response('Maybe', status=200)

    def find_media(self):
        dirs = os.listdir('repo')
        if 'media' in dirs:
            self.project['media_dir'] = 'media'
        elif 'resources' in dirs:
            self.project['media_dir'] = 'resources'


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
        print(os.listdir())

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



