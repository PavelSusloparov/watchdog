import logging

from django.shortcuts import render_to_response

log = logging.getLogger('main.views')

APPLICATIONS = {'trs': '/trs'}

def main(request):
    return render_to_response('main/main.html', {'host': request.META['HTTP_HOST'], 'applications': APPLICATIONS})
