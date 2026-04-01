#!/usr/bin/env python3
"""
Validate configuration consistency across krateo*.yaml files
This script is part of the krateoctl ecosystem for managing Krateo platform releases.

Checks: chart versions, chart repos/URLs, release names, and ALL image tags
Requires: PyYAML (installed via: pip install pyyaml)
"""

import sys
import glob
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ PyYAML is required but not installed.")
    print("   Install it with: pip install pyyaml")
    sys.exit(1)

print("📄 Extracting configuration from krateo*.yaml files...")
print("")
print("=" * 73)
print("CONFIGURATION CONSISTENCY CHECK")
print("=" * 73)
print("")

# Track all configurations by field
configs = defaultdict(lambda: {"values": {}, "files": {}})

# Fields to check for consistency: (field_name, extractor_function)
fields_to_check = [
    ("version", lambda step: step.get("with", {}).get("version")),
    ("repo", lambda step: step.get("with", {}).get("repo")),
    ("url", lambda step: step.get("with", {}).get("url")),
    ("releaseName", lambda step: step.get("with", {}).get("releaseName")),
]

# Find all krateo*.yaml files
krateo_files = sorted(glob.glob("./krateo*.yaml"))
if not krateo_files:
    print("❌ No krateo*.yaml files found!")
    sys.exit(1)

total_entries = 0

def extract_all_tags(values_dict, step_id):
    """
    Recursively extract all image tags from values section.
    Handles main image and nested component images (sidecars).
    """
    tags = []
    
    if not isinstance(values_dict, dict):
        return tags
    
    # Check for direct image.tag
    if "image" in values_dict and isinstance(values_dict["image"], dict):
        tag = values_dict["image"].get("tag")
        if tag:
            tags.append(("main", tag))
    
    # Check for nested component images (cdc, chartInspector, rdc, etc.)
    for component_name, component_config in values_dict.items():
        if isinstance(component_config, dict) and "image" in component_config:
            image_config = component_config["image"]
            if isinstance(image_config, dict):
                tag = image_config.get("tag")
                if tag:
                    tags.append((component_name, tag))
    
    return tags

# Extract configuration from each file
for file_path in krateo_files:
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        if not data or "steps" not in data:
            continue
        
        # Process each step
        for step in data.get("steps", []):
            step_id = step.get("id")
            if not step_id:
                continue
            
            # Extract standard fields
            for field_name, extractor in fields_to_check:
                value = extractor(step)
                
                if value is not None:  # Only track non-null values
                    total_entries += 1
                    key = f"{field_name}|{step_id}"
                    
                    # Track value occurrences
                    if key not in configs:
                        configs[key]["values"][value] = 1
                    else:
                        configs[key]["values"][value] = configs[key]["values"].get(value, 0) + 1
                    
                    # Track which files have this value
                    if file_path not in configs[key]["files"]:
                        configs[key]["files"][file_path] = value
            
            # Extract ALL image tags (main + nested sidecars)
            values_section = step.get("with", {}).get("values", {})
            all_tags = extract_all_tags(values_section, step_id)
            
            for component_name, tag_value in all_tags:
                total_entries += 1
                
                # Use component name in the key for clarity
                tag_field = f"tag_{component_name}" if component_name != "main" else "tag"
                key = f"{tag_field}|{step_id}"
                
                # Track value occurrences
                if key not in configs:
                    configs[key]["values"][tag_value] = 1
                else:
                    configs[key]["values"][tag_value] = configs[key]["values"].get(tag_value, 0) + 1
                
                # Track which files have this value
                if file_path not in configs[key]["files"]:
                    configs[key]["files"][file_path] = tag_value
    
    except yaml.YAMLError as e:
        print(f"⚠️  YAML error in {file_path}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
        sys.exit(1)

print(f"📊 Found {total_entries} configuration entries")
print("")

# Check for mismatches
mismatches = 0

for key, data in sorted(configs.items()):
    field_and_step = key.split("|", 1)
    field_name = field_and_step[0]
    step_id = field_and_step[1] if len(field_and_step) > 1 else ""
    
    values = data["values"]
    files = data["files"]
    
    if len(values) > 1:
        # Inconsistency detected
        expected_value = list(values.keys())[0]
        
        # Format display name
        if field_name.startswith("tag_"):
            component = field_name.replace("tag_", "")
            display_name = f"tag[{component}]"
        else:
            display_name = field_name
        
        print(f"⚠️  MISMATCH: {display_name}({step_id})")
        print(f"   Expected: {expected_value}")
        
        for file_path, actual_value in files.items():
            if actual_value != expected_value:
                print(f"   In {file_path}: {actual_value}")
        
        mismatches += 1

# Print summary
print("")
print("=" * 73)
print("")

if mismatches == 0:
    print("✅ All configurations are consistent across profiles!")
    print("")
    print("   Checked: chart versions, chart repositories & URLs,")
    print("            release names, and ALL image tags (main + sidecars)")
    print("")
    print("The GitHub Actions workflow will also validate this during CI/CD.")
    sys.exit(0)
else:
    print(f"❌ Found {mismatches} mismatch(es)!")
    print("")
    print("Please ensure all krateo*.yaml files have matching:")
    print("   • Chart versions")
    print("   • Chart repositories")
    print("   • Chart URLs")
    print("   • Release names")
    print("   • ALL image tags (main image + sidecar components)")
    sys.exit(1)

