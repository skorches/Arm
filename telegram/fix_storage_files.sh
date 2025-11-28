#!/bin/bash
# Fix Docker volume mount issues - convert directories to files

cd ~/Arm/telegram

echo "Stopping Docker container..."
docker-compose down

echo "Fixing storage files..."
# Remove directories and create files
for file in quiz_scores.json active_quizzes.json reading_progress.json daily_quiz.json achievements.json reminders.json quiz_history.json; do
    if [ -d "$file" ]; then
        echo "Removing directory: $file"
        rm -rf "$file"
    fi
    if [ ! -f "$file" ]; then
        echo "Creating file: $file"
        echo '{}' > "$file"
        chmod 666 "$file"
    fi
done

echo "Files fixed. Starting Docker container..."
docker-compose up -d --build

echo "Done! Check logs with: docker-compose logs -f"
