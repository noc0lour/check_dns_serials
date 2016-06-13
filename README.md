Python Secondary Namserver Serial Checker
================

Usage: call with /check_dns_serial.py domain1 domain2 domain3 domain4

If the serials returned from all nameservers of this domain are equal the script returns zero. Otherwise this script raises an exception providing information which domain has different DNS serials on their nameservers. 
For every nameserver the ip address is randomly picked from IPv4 and IPv6.

This script is designed to be run in a (hourly) cron job
