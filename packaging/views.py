import subprocess as sp

import requests

from rest_framework import viewsets
from rest_framework.response import Response


class PackageViewSet(viewsets.ViewSet):
    def post(self, request, *args, **kwargs):
        args = ['rm', '-rf', 'repo/']
        sp.call(args)

        url = request.data['url']
        args = ['git', 'clone', url, 'repo']
        sp.call(args)
        return Response()

