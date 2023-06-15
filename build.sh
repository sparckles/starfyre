#!/bin/sh

# RUSTUP_TOOLCHAIN=nightly maturin build --target wasm32-unknown-emscripten -i python3.10 --out dist
# cp dist/starfyre*.whl test-application/starfyre-dist

python3 starfyre --dev=True --path="test-application/" && python -m starfyre --build=True --path="test-application/"
