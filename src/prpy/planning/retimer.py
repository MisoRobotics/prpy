#!/usr/bin/env python

# Copyright (c) 2013, Carnegie Mellon University
# All rights reserved.
# Authors: Michael Koval <mkoval@cs.cmu.edu>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of Carnegie Mellon University nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import logging, numpy, openravepy, os, tempfile
from ..util import CopyTrajectory
from base import BasePlanner, PlanningError, PlanningMethod
from openravepy import PlannerStatus 

class OpenRAVERetimer(BasePlanner):
    def __init__(self, algorithm):
        super(OpenRAVERetimer, self).__init__()
        self.algorithm = algorithm

    @PlanningMethod
    def RetimeTrajectory(self, robot, path):
        RetimeTrajectory = openravepy.planningutils.RetimeTrajectory

        output_traj = CopyTrajectory(path, env=self.env)
        status = RetimeTrajectory(output_traj, False, 1., 1., self.algorithm)

        if status not in [ PlannerStatus.HasSolution,
                           PlannerStatus.InterruptedWithSolution ]:
            raise PlanningError('Retimer returned with status {0:s}.'.format(
                                str(status)))

        return output_traj

class ParabolicRetimer(OpenRAVERetimer):
    def __init__(self):
        super(ParabolicRetimer, self).__init__('ParabolicTrajectoryRetimer')