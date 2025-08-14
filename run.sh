#!/usr/bin/env bash
set -o errexit
gunicorn project.wsgi:application

