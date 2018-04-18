Simple Python script to rerun ElastiCube builds in case of failure.

This script gathers the last build time for an ElastiCube and runs the build if that time is farther in the past than a determined threshold.

Useful in cases where builds run overnight (say at 4 AM and last 45). Run the script at 5 AM; if the last build time is 4:45 AM on the day before (24+ hours ago), then this morning's build failed, and the script will kick off a new build.
