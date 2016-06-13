#!/usr/bin/env python3
# Copyright 2016 Andrej Rode.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

import dns.resolver
import dns.message
import dns.rdatatype
import sys


def check_serials(mydomain):
    ns_query = dns.resolver.query(mydomain, 'NS')
    nameservers = ns_query.rrset.items
    ns_list = [myns.to_text() for myns in nameservers]
    ns_dict = {}
    for ns in ns_list:
        ip_list = []
        try:
            ip4_query = dns.resolver.query(ns, 'A')
            for ip in ip4_query:
                ip_list += [ip.address]
        except:
            pass
        ns_dict.update({ns: frozenset(ip_list)})
        try:
            ip6_query = dns.resolver.query(ns, 'AAAA')
            for ip in ip6_query:
                ip_list += [ip.address]
        except:
            pass
        ns_dict.update({ns: frozenset(ip_list)})
    request = dns.message.make_query(mydomain, dns.rdatatype.SOA)
    serial_dict = {}
    for key in ns_dict.keys():
        name_server = list(ns_dict[key])[0]
        response = dns.query.udp(request, name_server)
        serial_dict.update({key: response.answer[0][0].serial})
    serial_values = list(serial_dict.values())
    if len(set(serial_values)) > 1:
        return(serial_dict)
    else:
        return 0


def main():
    args = sys.argv
    args.pop(0)
    errors = {}
    for domain in args:
        result = check_serials(domain)
        if result != 0:
            errors.update({domain: result})
    if errors :
        error_text = 'Serials in domain: {} are unequal. Returned serials from NS: {}\n'
        full_text = ''
        for key in errors.keys():
            full_text += error_text.format(key,errors[key])
        raise Exception(full_text)

if __name__ == "__main__":
    main()
