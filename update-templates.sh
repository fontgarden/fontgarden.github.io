#!/bin/bash

# Script to update header and footer in all HTML files

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if templates exist
if [ ! -f "templates/header.html" ] || [ ! -f "templates/footer.html" ]; then
    echo -e "${RED}Error: Template files not found in templates/ directory${NC}"
    exit 1
fi

# Read templates
HEADER_TEMPLATE=$(<templates/header.html)
FOOTER_TEMPLATE=$(<templates/footer.html)

# Function to extract page title from HTML comment
extract_page_title() {
    local file="$1"
    # Look for <!-- PAGE_TITLE: ... --> comment at the top of the file
    local title=$(grep -m1 '<!-- PAGE_TITLE:' "$file" | sed 's/.*PAGE_TITLE: *\(.*\) *-->/\1/')
    
    # If no title found, use filename without extension
    if [ -z "$title" ]; then
        title=$(basename "$file" .html | sed 's/^./\U&/')
    fi
    
    echo "$title"
}

# Process each HTML file
for file in *.html; do
    # Skip if no HTML files found
    [ ! -f "$file" ] && continue
    
    echo -e "${YELLOW}Processing: $file${NC}"
    
    # Create backup
    cp "$file" "$file.bak"
    
    # Extract page title
    PAGE_TITLE=$(extract_page_title "$file")
    
    # Replace {{PAGE_TITLE}} in header template
    HEADER_WITH_TITLE=$(echo "$HEADER_TEMPLATE" | sed "s/{{PAGE_TITLE}}/$PAGE_TITLE/g")
    
    # Create temporary file
    temp_file=$(mktemp)
    
    # Flag to track if we're in body
    in_body=false
    header_replaced=false
    footer_replaced=false
    
    # Process file line by line
    while IFS= read -r line; do
        # Check if we've entered the body tag
        if [[ "$line" =~ \<body ]]; then
            in_body=true
            echo "$line" >> "$temp_file"
            continue
        fi
        
        # If we're in body and haven't replaced header yet
        if [ "$in_body" = true ] && [ "$header_replaced" = false ]; then
            # Look for the header section start
            if [[ "$line" =~ \<div\ class=\"w-full\ px-4\ md:px-8\"\> ]]; then
                # Skip until we find the closing div after the navigation links
                echo "$HEADER_WITH_TITLE" >> "$temp_file"
                header_replaced=true
                
                # Skip lines until we find the end of the header section
                while IFS= read -r line; do
                    if [[ "$line" =~ \</div\> ]]; then
                        # Check if the next line is content or more navigation
                        IFS= read -r next_line
                        if [[ ! "$next_line" =~ \<a\ href.*\<h2 ]]; then
                            # We've found the end of header section
                            echo "$next_line" >> "$temp_file"
                            break
                        else
                            # Still in navigation, keep skipping
                            continue
                        fi
                    fi
                done
                continue
            fi
        fi
        
        # Look for footer
        if [[ "$line" =~ \<footer ]]; then
            # Skip the old footer
            echo "$FOOTER_TEMPLATE" >> "$temp_file"
            footer_replaced=true
            
            # Skip until we find </footer>
            while IFS= read -r line; do
                if [[ "$line" =~ \</footer\> ]]; then
                    break
                fi
            done
            continue
        fi
        
        # Write the line as-is
        echo "$line" >> "$temp_file"
        
    done < "$file"
    
    # Move temp file to original
    mv "$temp_file" "$file"
    
    # Remove backup if successful
    if [ $? -eq 0 ]; then
        rm "$file.bak"
        echo -e "${GREEN}✓ Updated: $file${NC}"
    else
        mv "$file.bak" "$file"
        echo -e "${RED}✗ Failed to update: $file (restored from backup)${NC}"
    fi
done

echo -e "${GREEN}Template update complete!${NC}"