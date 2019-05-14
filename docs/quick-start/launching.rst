####################
Launching
####################

Once the servers have been configured, they can be launched through the terminal:

.. code-block:: bash

  python3 app.py

Endpoints
==========

  By default, the servers are hosted at ``127.0.0.1:5000`` or ``localhost:5000``

``/routes``
***********
This is where the DroNeS program will obtain new or updated *routes* for the drones.

``/jobs``
*********
This is where the DroNeS program will obtain new or updated *jobs* for the drones.

``/update_timescale``
*********************
Whenever a simulation timescale changes, a request will be sent to this endpoint containing the updated timescale.

This is to ensure that the number of jobs generated per simulated second are in line with the simulation timescale.
