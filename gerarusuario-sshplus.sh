#!/bin/bash

usuario=$1
senha=$2
validade=$3
limite=$4

dataValidade=$(date "+%Y-%m-%d" -d "+$validade days")
password=$(perl -e 'print crypt($ARGV[0], "password")' $senha)

/usr/sbin/useradd -M -s /bin/false -e $dataValidade -p $password $usuario

if [ $? -eq 0 ]; then
    
    echo "usuario criado"
    echo "$senha" > /etc/SSHPlus/senha/$usuario
    echo "$usuario $limite" >> /root/usuarios.db
    
    fi
