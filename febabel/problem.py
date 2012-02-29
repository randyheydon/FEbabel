import os
from itertools import chain

from .common import Base, Switch


class FEproblem(Base):
    """A class to contain an entire finite element problem description."""

    def __init__(self, timestepper=None, options=None):
        self.timestepper = ( timestepper if timestepper is not None
                            else TimeStepper(0,0) )
        self.options = options if options is not None else dict()
        self.sets = dict()

    def get_children(self):
        s = set(chain( *self.sets.values() ))
        s.add(self.timestepper)
        return s


    def read(self, filename):
        """Convenience function to run the appropriate reader method.
        Currently guesses based on file extension."""
        ext = os.path.splitext(filename)[1][1:]
        getattr(self, 'read_%s'%ext)(filename)

    def write(self, filename):
        """Convenience function to run the appropriate writer method.
        Currently guesses based on file extension."""
        ext = os.path.splitext(filename)[1][1:]
        getattr(self, 'write_%s'%ext)(filename)



class TimeStepper(Base):
    """Dictates how the solution progresses through time.

    All values are floats.  max_step is currently an exception in that it can
    also be a LoadCurve object, as per FEBio's dtmax support.  This feature may
    eventually be dropped from FEbabel."""

    def __init__(self, duration, step_size, min_step=None, max_step=None):
        self.duration = duration
        self.step_size = step_size
        self.min_step = min_step
        self.max_step = max_step

    def get_children(self):
        if isinstance(self.max_step, Base):
            return set([self.max_step])
        else:
            return None


class SwitchTimeStepper(Switch, TimeStepper):
    """Acts as a container for TimeStepper objects that change with time, while
    presenting itself as a TimeStepper object."""
