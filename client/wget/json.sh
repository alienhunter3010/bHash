#!/bin/bash

json_escape() {
    echo $1 | sed 's#"#\\"#g'
}

json_pair() {
    echo \"$1\":\"`json_escape "$2"`\"
}

json_list() {
    sep=''
    for item in "$@" ; do
        echo -n $sep$item
        sep=','
    done
}

json_hash() {
    echo -n \{
    json_list "$@"
    echo \}
}

json_array() {
    echo -n \[
    json_list $@
    echo \]
}