#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys
from typing import Optional


class LibVersionBumper:
    def __init__(self) -> None:
        self.valid_bump_types = ["major", "minor", "patch"]
        self._sync_with_remote()

    def _parse_version(self, version_str: str) -> tuple[tuple[int, int, int], Optional[str]]:
        """Parse version string into components and optional suffix."""
        # Match versions like 1.2.3, 1.2.3-dev, 1.2.3-test, etc.
        match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9]+))?$", version_str)
        if not match:
            raise ValueError(f"Invalid version format: {version_str}")

        major, minor, patch = map(int, match.groups()[:3])
        suffix = match.group(4) if match.group(4) else None
        return (major, minor, patch), suffix

    def get_current_version(self) -> tuple[str, tuple[int, int, int], Optional[str]]:
        """Get the current version from git tags."""
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                capture_output=True,
                text=True,
                check=True,
            )
            current_version = result.stdout.strip().lstrip("v")

            version_tuple, suffix = self._parse_version(current_version)
            return current_version, version_tuple, suffix

        except subprocess.CalledProcessError:
            print("No existing tags found. Starting from v0.0.0")
            return "0.0.0", (0, 0, 0), None
        except ValueError as e:
            print(f"Error parsing version: {e}")
            sys.exit(1)

    def calculate_new_version(
        self,
        current_version: tuple[int, int, int],
        current_suffix: Optional[str],
        bump_type: str,
        new_suffix: Optional[str],
    ) -> str:
        """Calculate the new version based on bump type and suffix."""
        major, minor, patch = current_version

        # If current version has a suffix and we're not adding a new suffix, just remove the suffix
        if current_suffix is not None and new_suffix is None:
            version_str = f"{'.'.join(map(str, current_version))}"
        else:
            # Otherwise, bump version according to bump_type
            if bump_type == "major":
                new_version = (major + 1, 0, 0)
            elif bump_type == "minor":
                new_version = (major, minor + 1, 0)
            elif bump_type == "patch":
                new_version = (major, minor, patch + 1)
            else:
                raise ValueError(f"Invalid bump type: {bump_type}")

            version_str = f"{'.'.join(map(str, new_version))}"

        if new_suffix:
            version_str += f"-{new_suffix}"

        return version_str

    def create_and_push_tag(self, new_version: str, message: Optional[str] = None) -> None:
        """Create and push a new git tag."""
        try:
            # Check if tag already exists (on remote)
            self._sync_with_remote(tags_only=True)

            tag_version = f"{new_version}"
            result = subprocess.run(["git", "tag", "-l", tag_version], capture_output=True, text=True, check=True)
            if tag_version in result.stdout:
                print(f"Tag {tag_version} already exists!")
                sys.exit(1)

            # Create tag with message
            tag_message = message or f"Release {tag_version}"
            subprocess.run(["git", "tag", "-a", tag_version, "-m", tag_message], check=True)

            # Push tag
            subprocess.run(["git", "push", "origin", tag_version], check=True)
            print(f"Successfully created and pushed tag: {tag_version}")
            print(f"Tag message: {tag_message}")

        except subprocess.CalledProcessError as e:
            print(f"Error in git operations: {e}")
            sys.exit(1)

    def bump_version(
        self,
        bump_type: str,
        message: Optional[str] = None,
        suffix: Optional[str] = None,
        dry_run: bool = False,
    ) -> None:
        """Main function to bump version."""
        if bump_type not in self.valid_bump_types:
            print(f"Invalid bump type. Must be one of: {self.valid_bump_types}")
            sys.exit(1)

        # Get current version
        current_version_str, current_version_tuple, current_suffix = self.get_current_version()
        print(f"Current version: {current_version_str}{f'-{current_suffix}' if current_suffix else ''}")

        # Calculate new version
        new_version = self.calculate_new_version(current_version_tuple, current_suffix, bump_type, suffix)
        print(f"New version will be: {new_version}")
        if message:
            print(f"Tag message will be: {message}")

        if dry_run:
            print("Dry run: Would create tag:", new_version)
            return

        # Confirm with user
        if input("Proceed with version bump? [y/N]: ").lower() != "y":
            print("Version bump cancelled.")
            sys.exit(0)

        # Create and push tag
        self.create_and_push_tag(new_version, message)

    def _sync_with_remote(self, tags_only: bool = False) -> None:
        if tags_only:
            subprocess.run(["git", "fetch", "--tags"], capture_output=True, text=True, check=True)
        else:
            subprocess.run(["git", "fetch", "--all"], capture_output=True, text=True, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump version using git tags")
    parser.add_argument("bump_type", choices=["major", "minor", "patch"], help="Type of version bump")
    parser.add_argument("-m", "--message", help="Custom tag message (optional)")
    parser.add_argument("--suffix", help="Add a version suffix (e.g., 'dev', 'test')")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without making changes")

    args = parser.parse_args()

    try:
        bumper = LibVersionBumper()
        bumper.bump_version(args.bump_type, args.message, args.suffix, args.dry_run)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
