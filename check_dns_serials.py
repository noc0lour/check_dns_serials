#!/usr/bin/env python3
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
            continue
        try:
            ip6_query = dns.resolver.query(ns, 'AAAA')
            for ip in ip6_query:
                ip_list += [ip.address]
        except:
            continue
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
