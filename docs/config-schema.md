Config schema appendix
======================

This appendix documents the subset of VyOS boot configuration elements that
the matcher currently supports.

Root
----
```
firewall {
  global-options { state-policy { ... } }
  group { ... }
  ipv4 { ... }
  ipv6 { ... }
}
```

Global options
--------------
```
global-options {
  state-policy {
    established { action accept }
    related     { action accept }
    invalid     { action drop }
  }
}
```

Groups
------
Supported group types:
- `address-group`
- `network-group`
- `port-group`
- `interface-group`
- `ipv6-address-group`
- `ipv6-network-group`

Example:
```
group {
  network-group TRUSTEDv4 {
    network 192.0.2.0/30
    network 203.0.113.128/25
  }
  port-group WEBPORTS {
    port 80
    port 443
    port 8080-8090
  }
}
```

Base chains
-----------
```
ipv4 {
  forward {
    filter {
      default-action accept
      rule 10 { ... }
    }
  }
  input { filter { ... } }
  output { filter { ... } }
}
```

Named chains
------------
```
ipv4 {
  name CONN_FILTER {
    default-action return
    rule 10 { ... }
  }
}
```

Rule fields
-----------
Supported rule keys:
- `action` (accept, drop, reject, jump, continue, return)
- `jump-target`
- `protocol` (tcp, udp, icmp, icmpv6, tcp_udp, all, negation)
- `state` (established, related, new, invalid)
- `inbound-interface` / `outbound-interface`
- `source` / `destination`
- `icmp` / `icmpv6` (type-name)
- `disable`

Source/destination fields
-------------------------
```
source {
  address 192.0.2.10-192.0.2.20
  address-mask 255.255.255.255
  fqdn example.com
  port 443
  group {
    network-group TRUSTEDv4
    port-group WEBPORTS
  }
}
```

Notes
-----
- The CLI requires `--source` and `--destination` to be IPs; FQDNs are not
  accepted as input.
- If a rule has no destination criteria, it matches any destination.
