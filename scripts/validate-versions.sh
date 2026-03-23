#!/bin/bash
# Validate version consistency across krateo*.yaml files
# Portable for macOS and Linux

echo "📄 Extracting chart versions from krateo*.yaml files..."
echo ""
echo "======================================================================="
echo "VERSION CONSISTENCY CHECK"
echo "======================================================================="
echo ""

# Create temp file to store all versions
tmpfile=$(mktemp)
trap "rm -f $tmpfile" EXIT

# Extract all chart steps and their versions from all krateo*.yaml files
for file in ./krateo*.yaml; do
    if [ -f "$file" ]; then
        awk -v fname="$file" '/^  - id:/ {
            step_id = $3
            getline
            while ($0 !~ /^  - id:/ && NF > 0) {
                if ($0 ~ /version:/) {
                    version = $NF
                    print step_id "|" fname "|" version
                    break
                }
                getline
            }
        }' "$file" >> "$tmpfile"
    fi
done

# Use awk to check for consistency and report mismatches
awk -F'|' '
BEGIN {
    mismatches = 0
}
{
    step_id = $1
    file = $2
    version = $3
    
    if (!(step_id in versions)) {
        versions[step_id] = version
        print "✅ " step_id " → " version
    } else {
        if (versions[step_id] != version) {
            print "⚠️  MISMATCH: " step_id
            print "   Expected: " versions[step_id]
            print "   In " file ": " version
            mismatches++
        } else {
            print "✅ " step_id " → " version " (" file ")"
        }
    }
}
END {
    print ""
    print "======================================================================="
    print ""
    if (mismatches == 0) {
        print "✅ All chart versions are consistent across profiles!"
        print ""
        print "The GitHub Actions workflow will also validate this during CI/CD."
        exit 0
    } else {
        print "❌ Found " mismatches " version mismatch(es)!"
        print ""
        print "Please ensure all krateo*.yaml files have matching chart versions."
        exit 1
    }
}' "$tmpfile"

exit $?
