#!/bin/sh
# Fixture shell script for ShellParser TP suite
# top-level preamble (top-block)

hello() {
    echo "hello world"
}

greet() {
    name="${1:-world}"
    echo "hi ${name}"
}

# one-liner style
double_line() { output_text="ok"; echo "$output_text"; }
