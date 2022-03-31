#!/usr/bin/bash

sudo sed -i -E 's/^(josehu.*)(\/bin\/tcsh)$/\1\/bin\/bash/g' /etc/passwd
echo "Change shell to bash successful"
