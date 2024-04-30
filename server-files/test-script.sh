#!/bin/bash


while true; do
  echo Hello, who am I talking to?
  read -r varname
  echo It\'s nice to meet you "$varname"
  sleep 2
done