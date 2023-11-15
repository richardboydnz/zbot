find * -type d \( -name '.*' -o -name '__pycache__' \) -prune -o -type f -print   

find * -type d \( -name '.*' -o -name '__pycache__' \) -prune -o -type f -name '*.py' -exec grep -E '^(class |def )' {} +

find * -type d \( -name '.*' -o -name '__pycache__' \) -prune -o -type f -name '*.py' -exec sh -c 'echo "{}"; grep -E "^(class |def )" "{}"' \;
