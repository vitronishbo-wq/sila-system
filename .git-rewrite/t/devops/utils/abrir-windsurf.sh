#!/bin/bash

echo "🔧 Preparando ambiente gráfico para Windsurf..."

mount -t devpts devpts /dev/pts
mknod /dev/ptmx c 5 2
chmod 666 /dev/ptmx

echo "🚀 Tentando abrir Windsurf..."
scripts/misc/abrir-windsurf.sh
