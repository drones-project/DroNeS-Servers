####################
Scheduler
####################

The configuration file for the Scheduler (and comprising Job Generators) are in ``DroNeS-Servers/Scheduling/config.ini``

The following parameters are available:

Location Generation
===================
* ``dispatch_origin``

  This determines the center of a square that bounds that coordinates of jobs generated.

* ``dispatch_bounds``

  This determines the width and height of the square around the given `dispatch_origin` center.

List of Jobs
==============

Different types of jobs can be added by adding entries in the following format into the ``config.ini`` file::

  [Job:Pizza]
  Weight: 1
  Reward: 10
  Penalty: 30
  Valid_Time: 1800
  Cross_Section_Area: 0.25

* ``Weight`` - weight of the parcel in kilograms
* ``Reward`` - revenue gained from completing the job
* ``Penalty`` - penalty (or fine) incurred for failing to complete a job
* ``Valid_Time`` - the time (in seconds) in which the job must be completed by
* ``Cross_Section_Area`` - the effective cross sectional area of the parcel containing this item

Job Generation
==============
* ``params``

  This parameter is the λ parameter in a `Poisson distribution <https://en.wikipedia.org/wiki/Poisson_distribution>`_, and dictates the rate at which jobs will be generated (per second).
