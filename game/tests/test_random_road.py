# -*- coding: utf-8 -*-
# Code for Life
#
# Copyright (C) 2015, Ocado Innovation Limited
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ADDITIONAL TERMS – Section 7 GNU General Public Licence
#
# This licence does not grant any right, title or interest in any “Ocado” logos,
# trade names or the trademark “Ocado” or any other trademarks or domain names
# owned by Ocado Innovation Limited or the Ocado group of companies or any other
# distinctive brand features of “Ocado” as may be secured from time to time. You
# must not distribute any modification of this program using the trademark
# “Ocado” or claim any affiliation or association with Ocado or its employees.
#
# You are not authorised to use the name Ocado (or any of its trade names) or
# the names of any author or contributor in advertising or for publicity purposes
# pertaining to the distribution of this program, without the prior written
# authorisation of Ocado.
#
# Any propagation, distribution or conveyance of this program must include this
# copyright notice and these terms. You must not misrepresent the origins of this
# program; modified versions of the program must be marked as such and not
# identified as the original program.
from django.test import TestCase

import json
import random


def find_node(x, y, nodes):
    for node in nodes:
        if node['coordinate'][0] == x and node['coordinate'][1] == y:
            return True
    return False


def check_direction(node, neighbour):
    if neighbour['coordinate'][1] < node['coordinate'][1]:
        direction = "N"
    elif neighbour['coordinate'][0] < node['coordinate'][0]:
        direction = "E"
    elif neighbour['coordinate'][1] > node['coordinate'][1]:
        direction = "S"
    elif neighbour['coordinate'][0] > node['coordinate'][0]:
        direction = "W"
    return direction


class RandomRoadTestCase(TestCase):

    def create_test_data(self, num_tiles=None, branchiness=None, loopiness=None, curviness=None,
                         traffic_lights_enabled=False, decor_enabled=True, cows_enabled=False):
        if num_tiles is None:
            num_tiles = random.randint(3, 30)
        if branchiness is None:
            branchiness = random.randint(0, 10)
        if loopiness is None:
            loopiness = random.randint(0, 10)
        if curviness is None:
            curviness = random.randint(0, 10)

        from game.random_road import generate_random_map_data

        return generate_random_map_data(num_tiles, branchiness, loopiness, curviness,
                                        traffic_lights_enabled, decor_enabled, cows_enabled)

    def check_if_valid(self, origin, destinations, path, decor):
        check = find_node(origin['coordinate'][0], origin['coordinate'][1], path)
        self.assertTrue(check)

        for node in destinations:
            self.assertTrue(find_node(node[0], node[1], path))

        # Check if any decor got generated
        self.assertTrue(decor)

    def test_branchiness_min(self):

        """ Test that if the branchiness is 0 we don't get branches. """

        data = self.create_test_data(branchiness=0, loopiness=0, traffic_lights_enabled=False)

        path = json.loads(data['path'])
        destinations = json.loads(data['destinations'])
        traffic_lights = json.loads(data['traffic_lights'])
        origin = json.loads(data['origin'])
        decor = data['decor']

        self.check_if_valid(origin, destinations, path, decor)

        # Test if no branches
        for node in path:
            self.assertTrue(len(node['connectedNodes']) <= 2)

        # Assert no traffic lights got generated.
        self.assertFalse(traffic_lights)

    def test_curviness_max(self):
        """ Test that the path is curving significantly if the curviness is set to max value. """

        data = self.create_test_data(curviness=1, traffic_lights_enabled=False)

        path = json.loads(data['path'])
        destinations = json.loads(data['destinations'])
        traffic_lights = json.loads(data['traffic_lights'])
        origin = json.loads(data['origin'])
        decor = data['decor']

        self.check_if_valid(origin, destinations, path, decor)

        turn_count = 0
        for node in path:
            if len(node['connectedNodes']) > 1:
                turn_count += int(
                    not (check_direction(node, path[int(node['connectedNodes'][0])])
                         == check_direction(node, path[int(node['connectedNodes'][1])]))
                )

        # Check if there are any turns.
        self.assertTrue(turn_count)

        # Assert no traffic lights got generated.
        self.assertFalse(traffic_lights)
