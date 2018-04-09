
===============
Hello Websocket
===============


.. image:: https://img.shields.io/pypi/v/hello_websocket.svg
        :target: https://pypi.python.org/pypi/hello_websocket

.. image:: https://img.shields.io/travis/justdoit0823/hello_websocket.svg
        :target: https://travis-ci.org/justdoit0823/hello_websocket

.. image:: https://readthedocs.org/projects/hello-websocket/badge/?version=latest
        :target: https://hello-websocket.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


===========
Get Started
===========

Dependency
------------

* Python3.5+

* Rabbitmq server


Requirements
--------------

* requirements.txt

This file contains packages to run the websocket client and server program, such as `aiohttp`, `click`, `aio-pika`.


* requirements_dev.txt

This file contains packages to develop this project.


QuickStart
------------

First, create a virtual environment.

.. code-block:: bash

   $ python3 -m venv hello_venv
   $ source hello_venv/bin/activate
   $ pip install -r requirements.txt

Then, start the local rabbitmq server. And run the websocket server.

.. code-block:: bash

   $ python hello_websocket/server.py run
   amqp://guest:********@127.0.0.1:5672//
   ======== Running on http://127.0.0.1:8989 ========
   (Press CTRL+C to quit)
   receive message d888aba59857c5a373a48f03718beec3ebd69180ff710a537183c807059c5b3f from 123456.
   receive message 1d516b32b579d1094e02ee9fab70eedf073cf3805e1ff924a3a7e2e24c06f1ef from 123456.
   receive message a342df31c60783eec7d1bfbe4ad75284d7d0a4807d79609a2189d5ca7640390f from 123456.


Now, start the websocket client program.

.. code-block:: bash

   $ python hello_websocket/client.py run 123456
   receive message hello
   receive message hello world
   receive message hello from http endpoint


Send message to the websocket client.

.. code-block:: bash

   $ http "http://127.0.0.1:8989/pub?token=123456&body=hello from http endpoint"
   HTTP/1.1 200 OK
   Content-Length: 2
   Content-Type: text/plain; charset=utf-8
   Date: Mon, 09 Apr 2018 12:39:20 GMT
   Server: Python/3.6 aiohttp/3.1.2

   ok


========
Features
========

* bidirectional communication between clients and server.

* push message api.


=======
Credits
=======


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
