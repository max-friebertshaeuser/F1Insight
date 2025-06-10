#!/bin/bash

# List of directories to create
dirs=(
  "src/assets"
  "src/components/Button"
  "src/pages/Home"
  "src/hooks"
  "src/contexts"
  "src/services"
  "src/utils"
)

# Create directories
for dir in "${dirs[@]}"; do
  mkdir -p "$dir"
done

# List of files to create with their full paths
files=(
  "src/components/Button/Button.tsx"
  "src/components/Button/Button.test.tsx"
  "src/pages/Home/Home.tsx"
  "src/pages/Home/Home.test.tsx"
  "src/hooks/useFetch.ts"
  "src/contexts/ThemeContext.tsx"
  "src/services/ergastAPI.ts"
  "src/utils/formatDate.ts"
  "src/App.tsx"
  "src/index.tsx"
  "src/routes.tsx"
)

# Create files if they don't already exist
for file in "${files[@]}"; do
  if [ ! -f "$file" ]; then
    touch "$file"
  fi
done

echo "Project structure created! 🚀"
