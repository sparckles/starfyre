#!/bin/sh

python3 starfyre --dev=True --path="test-application/" && python -m starfyre --build=True --path="test-application/"
