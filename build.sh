#!/bin/sh

RUSTUP_TOOLCHAIN=nightly maturin build --target wasm32-unknown-emscripten -i python3.10 --out dist
cp dist/starfyre-0.1.0-cp310-cp310-emscripten_3_1_27_wasm32.whl test-application/starfyre-dist
