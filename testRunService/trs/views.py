import os
import logging

from django.http import Http404
from django.shortcuts import render_to_response
from models import Test
from forms import TestForm

log = logging.getLogger('trs.views')


def index(request):
    """
    Function handle index page form views and GET requests.
    @request: request to /trs page.
    @return: handled request as template with arguments.
    """
    try:
        tests = Test.objects.all()
        for test in tests:
            setattr(test, 'name', test.path.split('/')[-1])

        #Handle GET request
        if request.method == 'GET':
            form = TestForm(request.GET)
            if form.is_valid():
                log.debug('index:GET: Get path: %s' % form.cleaned_data['path'])
                log_file_full_path = form.cleaned_data['path'][:-3] + '.log'
                log.debug("index:GET: log_file_full_path: %s" % log_file_full_path)
                if request.GET.has_key('run'):
                    test_status = {}
                    # Remove .py postfix and add .log
                    status = os.system('python %s > %s' % (form.cleaned_data['path'], log_file_full_path))
                    log.debug("index:GET:run: status: %s" % status)
                    if status != 0:
                        test_status['color'] = 'red'
                        if status == 256:
                            test_status['msg'] = 'Test is fail. Please check %s' % log_file_full_path
                        else:
                            test_status['msg'] = 'Can not find test. Please provide correct pass.'
                        log.warning('index:GET:run: %s file can not be run. Reason: %s' %
                                    (form.cleaned_data['path'], test_status['msg']))
                    else:
                        test_status['color'] = 'green'
                        test_status['msg'] = 'Test was finished.'
                        log.debug('index:GET:run: test_status: %s' % test_status)

                    return render_to_response('trs/run.html', {'tests': tests, 'test_status': test_status})
                elif request.GET.has_key('show'):
                    logfile = []
                    show_error = 'Logfile is not exist or empty.'
                    show_result = ''
                    try:
                        for line in open(log_file_full_path):
                            logfile.append(line)
                            log.debug("index:GET:show: logfile: %s" % logfile)
                    except:
                        show_result = show_error
                        log.warning("index:GET:show: %s file can not be showen." % form.cleaned_data['path'])
                    if not logfile:
                        show_result = show_error
                        log.warning("index:GET:show: %s file can not be showen. Reason: %s" %
                                    (form.cleaned_data['path'], show_error))

                    return render_to_response('trs/show.html', {'tests': tests, 'test_result': logfile,
                                                                'show_result': show_result})
            else:
                log.warning('Form %s is not valid.')
        return render_to_response( 'trs/index.html', {'tests': tests})
    except Exception as e:
        log.error("index: %s" % e)
        raise Http404
