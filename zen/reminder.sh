#!/bin/bash
# 🧘 Mindfulness Reminder System
# Place in crontab or run as background service
# Add to crontab with: crontab -e

# Configuration
USER_NAME="${USER:-friend}"
LOG_FILE="${HOME}/.openclaw/workspace/zen/reminders.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Function to send gentle reminder
remind() {
    local message="$1"
    local icon="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $icon $message" >> "$LOG_FILE"
    
    # If notify-send is available (Linux desktop)
    if command -v notify-send &> /dev/null; then
        notify-send -i "face-cool" -t 5000 "Mindfulness" "$icon $message"
    fi
    
    # If running in terminal
    echo -e "\n🧘 $icon $message 🧘\n"
}

# Parse command or time-based trigger
case "${1:-$(date +%H:%M)}" in
    # Morning
    morning|06:00|06:30|07:00)
        remind "Good morning, $USER_NAME. Set your intention with 3 breaths." "🌅"
        ;;
    
    # Hourly work reminders
    :00|hourly)
        remind "Micro-pause: 3 conscious breaths. Soften your eyes." "⏰"
        ;;
    
    :30|half-hour)
        remind "Posture check: Spine tall, shoulders down, jaw unclenched." "🪑"
        ;;
    
    # Lunch
    12:00|lunch)
        remind "Mindful lunch: Eat without screens. Taste each bite." "🍽️"
        ;;
    
    # Afternoon reset
    15:00|afternoon)
        remind "Nature reset: Step outside. Feel sun. Take 10 breaths." "🌿"
        ;;
    
    # Evening transition
    18:00|evening)
        remind "Transition ritual: Change clothes. Leave work behind." "🌆"
        ;;
    
    # Digital sunset
    20:00|sunset)
        remind "Digital sunset begins. Dim screens. Rest your mind." "🌙"
        ;;
    
    # Gratitude
    20:30|gratitude)
        remind "Gratitude pause: Three things that went well today." "✨"
        ;;
    
    # Wind down
    21:00|wind-down)
        remind "Prepare for rest. Release the day with compassion." "😴"
        ;;
    
    # Manual triggers
    breathe|breath)
        remind "Take 3 deep breaths. In... hold... out..." "🫁"
        ;;
    
    focus|work)
        remind "Focus mode: Single task. Phone away. Begin with breath." "🎯"
        ;;
    
    stress|calm|anxiety)
        remind "4-7-8 breath: In 4, Hold 7, Out 8. You are safe." "🌊"
        ;;
    
    stop)
        remind "STOP: Stop. Take breath. Observe. Proceed with care." "🛑"
        ;;
    
    body)
        remind "Body scan: Shoulders? Jaw? Hands? Belly? Release tension." "🧍"
        ;;
    
    *)
        echo "🧘 Mindfulness Reminder System"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Time-based:"
        echo "  morning, hourly, half-hour, lunch, afternoon"
        echo "  evening, sunset, gratitude, wind-down"
        echo ""
        echo "Manual triggers:"
        echo "  breathe, focus, stress, stop, body"
        echo ""
        echo "Or run with cron for automatic reminders."
        ;;
esac
