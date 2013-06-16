import logging

from django import forms
from trs.models import Test

log = logging.getLogger('trs.forms')

class TestForm(forms.Form):
    """
    Form of test attributes.
    """
    path=forms.CharField(max_length=100)
