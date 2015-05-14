#!/usr/bin/env bash

keytool -genkey -v -keystore $1.keystore -alias $2 -keyalg RSA -keysize 2048 -validity 10000
