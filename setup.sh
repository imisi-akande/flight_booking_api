#!/bin/bash

set -e
set -o pipefail

function flightbooking() {
    echo 'Do you have virtualenv installed on your machine?'
    echo "Enter y or n"

    read response
  
    if [ $response == "y" ]; then
      echo "Do you want to activate the environment for your project?"
      echo "y or n"
  
      read answer
  
      if [ $answer == "y" ]; then
        virtualenv --python=python3
        source flightbooking/bin/activate
        echo "Your virtual environment has been activated.."
      else
        echo "It appears there is an existing development environment setup"
      fi
    else
      echo "Do you want it to be installed an activated as well"
      echo  "y or n"

      read response
  
      if [ $response == "y" ]; then
        pip install virtualenv
        virtualenv --python=python3 flightbooking
        source flightbooking/bin/activate
        echo "Your virtual environment has been activated"
      else
        echo "It appears there is an existing development environment"
      fi
    fi
}

flightbooking
