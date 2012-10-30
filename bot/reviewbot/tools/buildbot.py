import os

from reviewbot.processing.filesystem import make_tempfile
from reviewbot.tools.process import execute
from reviewbot.tools import Tool


class buildbot(Tool):
    name = 'BuilBot try plugin'
    version = '0.1'
    description = "Attempt to build given diff on your buildbot servers"
    options = [
        {
            'name': 'address',
            'field_type': 'django.forms.CharField',
            'default': None,
            'field_options': {
                'label': 'Buildmaster Address',
                'help_text': 'The address of the buildmaster. Used by both PB\
                 and SSH',
                'required': True,
            },
        },
        {
            'name': 'connect_method',
            'field_type': 'django.forms.ChoiceField',
            'default': True,
            'field_options': {
                'label': 'Connect Method',
                'help_text': 'Connection method used by buildbot to contact \
                 the try server',
                'required': True,
                'choices': (('PB', 'PB authentication'),
                            ('SSH', 'SSH authentication')
                            ),
            }
        },
        {
            'name': 'port',
            'field_type': 'django.forms.CharField',
            'default': None,
            'field_options': {
                'label': 'Port',
                'help_text': 'Connection port. If using PB, enter the port the\
                 try scheduler is listening on. If using SSH, enter the port of\
                  the SSH server (usually 22)',
                'required': True,
            },
        },
        {
            'name': 'username',
            'field_type': 'django.forms.CharField',
            'default': None,
            'field_options': {
                'label': 'username',
                'help_text': 'Username, used by both PB and SSH authentication',
                'required': True,
            },
        },
        {
            'name': 'password',
            'field_type': 'django.forms.CharField',
            'default': None,
            'field_options': {
                'label': 'PB Password',
                'help_text': 'PB Password: improperly stored. Use with caution',
                'required': False,
            },
        },
        {
            'name': 'jobdir',
            'field_type': 'django.forms.CharField',
            'default': None,
            'field_options': {
                'label': 'job dir',
                'help_text': 'SSH Job dir: Directory chosen in buildbot config\
                 to be writeable by all allowed users',
                'required': False,
            },
        },
        {
            'name': 'pblistener',
            'field_type': 'django.forms.CharField',
            'default': None,
            'field_options': {
                'label': 'PB listener port',
                'help_text': 'Required when using SSH. Indicate port used to\
                 check build status',
                'required': False,
            },
        },
        {
            'name': 'buildbotbin',
            'field_type': 'django.forms.CharField',
            'default': None,
            'field_options': {
                'label': 'buildbot binary location',
                'help_text': 'SSH buildbot binary location: path to buildbot if\
                 not in user\'s path. For use with virtualenv',
                'required': False,
            },
        },
    ]

    def execute(self):
        diff = make_tempfile(self.review.diff.diff)

        if self.settings['connect_method'] == 'PB':
            output = execute(
                [
                    'buildbot',
                    'try',
                    '--wait',
                    '--connect=pb',
                    '--username=%s' % self.settings['username'],
                    '--master=%s:%s' % (self.settings['address'],
                                        self.settings['port']
                                        ),
                    '--passwd=%s' % self.settings['password'],
                    '--diff=%s' % os.path.abspath(diff),
                    '--patchlevel=1',
                ],
                ignore_errors=True)
        else:
            #TODO SSH
            print("yeah...")

        self.review.body_top = "Buildbot Result:\n%s" % output
