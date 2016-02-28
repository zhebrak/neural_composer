#!/bin/sh

timidity -Ow -o - $1 | lame - $2
