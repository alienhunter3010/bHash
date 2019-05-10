#!/bin/bash

. json.sh

baseurl="http://localhost"

function signup() {
    local password=''
    local password2=''
    local login=$1
    echo "Hello $1, you are going to register on bHash"
    while (true) ; do
        echo -n 'Insert password '
        read -s password
        echo
        echo -n 'Insert again '
        read -s password2
        echo
        if [ `echo $password | wc -c` -lt 6 ] ; then
            echo -n Password must have at least 6 characters.
        elif [ "x$password" != "x$password2" ] ; then
            echo -n Passwords do not match.
        else
            break
        fi
        echo ' Try Again, Ctrl+C to abort'
    done
    local email=''
    local additional=''
    local auth="username=$login&password=$password"
    echo -n 'You can add an email registered on gravatar.com '
    read email
    if [ "x$email" != "x" ] ; then
        additional="&email=$email"
    fi
    wget --post-data $auth$additional $baseurl/s/register -qO-
    if [ $? == 0 ] ; then
	echo
        token=`wget --post-data $auth $baseurl/s/token -qO-`
    else
        echo Error detected, try again
    fi
}

function signin() {
    local password=''
    local login=$1
    echo "Hello $1, you need a token"
    echo -n 'Insert password'
    read -s password
    echo

    token=`wget --post-data "username=$login&password=$password" $baseurl/s/token -qO-`
}

function publish() {
    if [ "x$token" == "x" ] ; then
        echo 'You need a token'
        echo 'Please use'
        echo '  signin <username>'
        echo 'and try again.'
        echo 'If you have no account on bHash use'
        echo '  signup <username>'
        return
    fi
    local tag='test'
    local image=''
    while true ; do
        case "$1" in
            -t|--tags)
                shift
                tag=`echo "#$1" | sed 's/,/#/g'`
                ;;
            -i|--image)
                shift
                image=$1
                ;;
            --)
                break
                ;;
            *)
                break
                ;;
        esac
        shift
    done
    local post=''
    while read row ; do
        post="$post$row
"
    done

    wget --post-data "token=$token&tags=$tag&content=$post" $baseurl/s/publish -qO-
}

content() {
    local image=''
    local content=''
    while true ; do
        case "$1" in
            -m|--markdown)
                shift
                content=`json_pair md "$1"`
                ;;
            -c|--content)
                shift
                content=`json_pair content $1`
                ;;
            -i|--image)
                shift
                image=`json_pair img $1`
                ;;
            --)
                break
                ;;
            *)
                break
                ;;
        esac
        shift
    done

    json_hash "$content" $image
}
