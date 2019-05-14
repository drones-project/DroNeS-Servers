###################
Basic Installation
###################

These instructions cover an installation from the master branch in git.

Prerequisites
*************

Follow one of the guides below to get the basic prerequisites installed:

.. toctree::
    :titlesonly:
    :maxdepth: 2
    :glob:

    osx
    windows
    linux

Downloading the Application
***************************

To run a copy from the latest ``master`` branch in ``git`` you can clone the repository:

.. code-block:: bash

  git clone --recursive https://github.com/chowder/DroNeS-Servers


Installing Python dependencies
******************************

At this point you should have the following:

* Python 3.6.x
* pip
* DroNeS-Servers application folder

First, open up a shell (``cmd.exe`` or ``terminal.app``) and ``cd`` into the ``DroNeS-Servers`` directory.

Now you can install all the Python dependencies:

.. code-block:: bash

  pip install -r requirements.txt


Installation complete
******************************

The installation stage is complete, head to the Quick Start section to learn how to configure and run the servers.
