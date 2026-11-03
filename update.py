import os
import json
from datetime import datetime, timezone

def main():
    packages_dir = "packages"
    index_file = "index.json"
    
    index_data = {
        "registry_version": 1,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "packages": {}
    }

    if not os.path.isdir(packages_dir):
        print(f"Error: '{packages_dir}' directory not found.")
        return

    # Iterate through package directories (e.g., jsoner, qeloquent, restlink)
    for pkg_name in sorted(os.listdir(packages_dir)):
        pkg_path = os.path.join(packages_dir, pkg_name)
        if not os.path.isdir(pkg_path):
            continue

        meta_file = os.path.join(pkg_path, "meta.json")
        if not os.path.isfile(meta_file):
            print(f"Warning: Skipping '{pkg_name}' — missing meta.json")
            continue

        # Load package metadata
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception as e:
            print(f"Error parsing {meta_file}: {e}")
            continue

        # Discover all version json files (e.g., 1.4.2.json -> version "1.4.2")
        versions = []
        for filename in os.listdir(pkg_path):
            if filename.endswith(".json") and filename != "meta.json":
                version_str = filename[:-5]  # Strip '.json'
                if version_str.startswith('v'):
                    version_str = version_str.removeprefix('v')
                versions.append(version_str)

        if not versions:
            print(f"Warning: Package '{pkg_name}' has no version manifests.")
            continue

        # Sort versions (standard alphabetical or reverse sort)
        versions.sort(key=lambda s: [int(u) if u.isdigit() else u for u in s.replace('-', '.').split('.')])
        versions.reverse() # Latest/highest version first
        
        latest_version = versions[0]

        # Register package in index
        index_data["packages"][pkg_name] = {
            "display_name": meta.get("display_name", pkg_name.capitalize()),
            "description": meta.get("description", ""),
            "latest": latest_version,
            "versions": versions
        }

    # Write out index.json
    try:
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(index_data, f, indent=2)
        print(f"Successfully generated {index_file} with {len(index_data['packages'])} packages.")
    except Exception as e:
        print(f"Error writing {index_file}: {e}")

if __name__ == "__main__":
    main()
