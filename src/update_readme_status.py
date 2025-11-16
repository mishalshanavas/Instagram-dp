"""
Update README.md with current status information
This script safely updates only the status section between markers
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
import re

# Get repository root
REPO_ROOT = Path(__file__).parent.parent
README_PATH = REPO_ROOT / "README.md"
INDEX_FILE = REPO_ROOT / "data" / "index.txt"
LAST_RUN_FILE = REPO_ROOT / "data" / "last_run.txt"
NEXT_SCHEDULED_FILE = REPO_ROOT / "data" / "next_scheduled.txt"
CONFIG_FILE = REPO_ROOT / "data" / "config.json"

# Markers for the status section
START_MARKER = "<!-- STATUS_START -->"
END_MARKER = "<!-- STATUS_END -->"


def get_current_index():
    """Get current image index"""
    if INDEX_FILE.exists():
        try:
            return int(INDEX_FILE.read_text().strip())
        except:
            return 0
    return 0


def get_last_run_time():
    """Get last run timestamp"""
    if LAST_RUN_FILE.exists():
        try:
            timestamp = int(LAST_RUN_FILE.read_text().strip())
            return datetime.fromtimestamp(timestamp)
        except:
            return None
    return None


def get_next_scheduled_time():
    """Get next scheduled run timestamp"""
    if NEXT_SCHEDULED_FILE.exists():
        try:
            timestamp = int(NEXT_SCHEDULED_FILE.read_text().strip())
            return datetime.fromtimestamp(timestamp)
        except:
            return None
    return None


def get_timezone():
    """Get configured timezone"""
    if CONFIG_FILE.exists():
        try:
            config = json.loads(CONFIG_FILE.read_text())
            return config.get("timezone", "UTC")
        except:
            return "UTC"
    return "UTC"


def get_total_images():
    """Count total images in assets/images"""
    images_folder = REPO_ROOT / "assets" / "images"
    if images_folder.exists():
        images = [f for f in images_folder.iterdir() 
                 if f.suffix.lower() in ['.png', '.jpg', '.jpeg']]
        return len(images)
    return 0


def format_time_ago(dt):
    """Format datetime as 'X hours ago' or similar"""
    if dt is None:
        return "Never"
    
    now = datetime.now()
    diff = now - dt
    
    if diff.total_seconds() < 60:
        return "Just now"
    elif diff.total_seconds() < 3600:
        mins = int(diff.total_seconds() / 60)
        return f"{mins} min{'s' if mins != 1 else ''} ago"
    elif diff.total_seconds() < 86400:
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:
        days = int(diff.total_seconds() / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"


def format_time_until(dt):
    """Format datetime as 'In X hours' or similar"""
    if dt is None:
        return "Not scheduled"
    
    now = datetime.now()
    diff = dt - now
    
    if diff.total_seconds() < 0:
        return "Overdue"
    elif diff.total_seconds() < 60:
        return "In < 1 min"
    elif diff.total_seconds() < 3600:
        mins = int(diff.total_seconds() / 60)
        return f"In ~{mins} min"
    elif diff.total_seconds() < 86400:
        hours = int(diff.total_seconds() / 3600)
        mins = int((diff.total_seconds() % 3600) / 60)
        return f"In ~{hours}h {mins}m"
    else:
        days = int(diff.total_seconds() / 86400)
        hours = int((diff.total_seconds() % 86400) / 3600)
        return f"In ~{days}d {hours}h"


def generate_status_section():
    """Generate the status section content"""
    current_idx = get_current_index()
    total_images = get_total_images()
    next_idx = (current_idx + 1) % total_images if total_images > 0 else 0
    
    last_run = get_last_run_time()
    next_scheduled = get_next_scheduled_time()
    timezone = get_timezone()
    
    # Format timestamps
    last_run_str = format_time_ago(last_run)
    next_run_str = format_time_until(next_scheduled)
    next_time_str = next_scheduled.strftime("%H:%M %Z") if next_scheduled else "Not scheduled"
    
    status_content = f"""{START_MARKER}

## Live Status

<div align="center">

| Current DP | Next DP | Status |
|:----------:|:-------:|:------:|
| <img src="./assets/images/{current_idx + 1}.png" width="150" alt="Current DP"> | <img src="./assets/images/{next_idx + 1}.png" width="150" alt="Next DP"> | ⏰ **{next_run_str}** |
| **Image {current_idx + 1} of {total_images}** | **Image {next_idx + 1} of {total_images}** | Next: {next_time_str} {timezone} |

**Last Updated:** {last_run_str} • **Total Images:** {total_images}

</div>

{END_MARKER}"""
    
    return status_content


def update_readme():
    """Update README.md with new status section"""
    if not README_PATH.exists():
        print("❌ README.md not found")
        return False
    
    # Read current README
    readme_content = README_PATH.read_text()
    
    # Generate new status section
    new_status = generate_status_section()
    
    # Check if markers exist
    if START_MARKER in readme_content and END_MARKER in readme_content:
        # Replace existing status section
        pattern = f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}"
        updated_content = re.sub(pattern, new_status, readme_content, flags=re.DOTALL)
    else:
        # Add status section after the main heading and demo
        # Find the position after the demo/badges section
        lines = readme_content.split('\n')
        insert_pos = 0
        
        # Find a good position (after badges/demo, before "Quick Setup" or first ##)
        for i, line in enumerate(lines):
            if line.startswith('## ') or line.startswith('> **TL;DR'):
                insert_pos = i
                break
        
        # Insert the status section
        lines.insert(insert_pos, new_status + '\n')
        updated_content = '\n'.join(lines)
    
    # Write updated README
    README_PATH.write_text(updated_content)
    print("✅ README.md updated with current status")
    return True


if __name__ == "__main__":
    update_readme()
