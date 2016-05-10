# Copyright 2012-2014 eNovance <licensing@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys

from oslo_config import cfg
import oslo_i18n
from oslo_log import log
from oslo_reports import guru_meditation_report as gmr

from panko.conf import defaults
from panko import version


def prepare_service(argv=None, config_files=None):
    oslo_i18n.enable_lazy()
    log.register_options(cfg.CONF)
    defaults.set_cors_middleware_defaults()

    if argv is None:
        argv = sys.argv
    cfg.CONF(argv[1:], project='panko', validate_default_values=True,
             version=version.version_info.version_string(),
             default_config_files=config_files)

    log.setup(cfg.CONF, 'panko')
    # NOTE(liusheng): guru cannot run with service under apache daemon, so when
    # panko-api running with mod_wsgi, the argv is [], we don't start
    # guru.
    if argv:
        gmr.TextGuruMeditation.setup_autorun(version)