#!/bin/sh

# RUSTUP_TOOLCHAIN=nightly maturin build --target wasm32-unknown-emscripten -i python3.10 --out dist
# cp dist/starfyre*.whl test-application/starfyre-dist

maturin develop && python3 starfyre test-application && python -m test-application
