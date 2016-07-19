# coding=utf-8

# Copyright (c) 2001-2016, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io
import os
import pytest
import tartare
import tartare.api
import json


@pytest.fixture(scope="module")
def app():
    return tartare.app.test_client()


def to_json(response):
    return json.loads(response.data.decode('utf-8'))


def test_post_grid_calendar_returns_success_status(app):
    r = app.post('/grid_calendar')
    assert '200 OK' in r.status


def test_unkown_version_status(app):
    raw = app.get('/status')
    r = to_json(raw)
    assert raw.status_code == 200
    assert r.get('version') == 'unknown_version'


def test_kown_version_status(app, monkeypatch):
    """if TARTARE_VERSION is given at startup, a version is available"""
    version = 'v1.42.12'
    monkeypatch.setitem(os.environ, 'TARTARE_VERSION', version)
    raw = app.get('/status')
    r = to_json(raw)
    assert raw.status_code == 200
    assert r.get('version') == version