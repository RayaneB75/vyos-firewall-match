"""Decision Engine - Minimal firewall matching logic.

Evaluates traffic tuples against firewall rules using a top-down first-match approach.
"""

import ipaddress
from typing import Optional

from vyfwmatch.domain.models import (
    Chain,
    FirewallConfig,
    InterfaceCriteria,
    MatchResult,
    Rule,
    SourceDestCriteria,
    TrafficTuple,
)

# Import existing helper functions for matching logic
from matcher.helpers import (
    interface_matches,
    ip_matches,
    ip_matches_with_mask,
    port_matches,
    protocol_matches,
)


class DecisionEngine:
    """Minimal firewall matching engine.

    Evaluates traffic against firewall rules using top-down first-match logic.
    """

    def __init__(self, config: FirewallConfig):
        """Initialize the engine with firewall configuration.

        Args:
            config: Loaded firewall configuration
        """
        self.config = config

    def match(self, traffic: TrafficTuple) -> MatchResult:
        """Match traffic against firewall configuration.

        Args:
            traffic: Traffic tuple to evaluate

        Returns:
            MatchResult with verdict and trace information
        """
        result = MatchResult()

        # Determine hook
        hook = self._determine_hook(traffic)
        result.trace.append(f"Hook determined: {hook}")

        # Determine family
        family = self._determine_family(traffic)
        result.chain_family = family
        result.chain_hook = hook

        # Get chains for this family
        chains = self.config.ipv4_chains if family == "ipv4" else self.config.ipv6_chains

        # Find the base chain
        chain_key = f"{hook}-filter"
        chain = chains.get(chain_key)

        if chain is None:
            result.trace.append(f"No {family} {chain_key} chain found")
            result.matched = True
            result.action = "accept"
            result.is_default_action = True
            result.chain_name = chain_key
            return result

        # Evaluate the chain
        chain_result = self._evaluate_chain(chain, traffic, chains, result.trace)

        # Check state-policy as fallback before default-action
        if chain_result.matched and not chain_result.is_default_action:
            return chain_result

        state_result = self._check_state_policy(traffic)
        if state_result is not None:
            return state_result

        return chain_result

    def _determine_hook(self, traffic: TrafficTuple) -> str:
        """Determine hook from traffic tuple."""
        if traffic.hook:
            return traffic.hook
        return "forward"

    def _determine_family(self, traffic: TrafficTuple) -> str:
        """Determine IPv4 or IPv6 from traffic IPs."""
        for ip_str in (traffic.source_ip, traffic.destination_ip):
            if ip_str:
                try:
                    addr = ipaddress.ip_address(ip_str)
                    if addr.version == 6:
                        return "ipv6"
                except ValueError:
                    pass
        return "ipv4"

    def _check_state_policy(self, traffic: TrafficTuple) -> Optional[MatchResult]:
        """Check global state-policy."""
        if not traffic.state or not self.config.state_policies:
            return None

        for sp in self.config.state_policies:
            if sp.state == traffic.state:
                return MatchResult(
                    matched=True,
                    action=sp.action,
                    is_state_policy=True,
                    state_policy_state=sp.state,
                    trace=[f"Global state-policy match: state={sp.state} -> {sp.action}"],
                )
        return None

    def _evaluate_chain(
        self,
        chain: Chain,
        traffic: TrafficTuple,
        all_chains: dict[str, Chain],
        trace: list[str],
    ) -> MatchResult:
        """Evaluate rules in a chain top-down."""
        trace.append(f"Evaluating chain: {chain.family} {chain.name}")

        for rule in chain.sorted_rules():
            if rule.disabled:
                trace.append(f"  Rule {rule.number}: DISABLED, skipping")
                continue

            if self._rule_matches(rule, traffic, trace):
                trace.append(f"  Rule {rule.number}: MATCHED -> action={rule.action}")

                if rule.action == "jump" and rule.jump_target:
                    trace.append(f"  Jumping to chain: {rule.jump_target}")
                    target_chain = all_chains.get(rule.jump_target)
                    if target_chain is None:
                        trace.append(f"  Jump target '{rule.jump_target}' not found!")
                        continue

                    sub_result = self._evaluate_chain(target_chain, traffic, all_chains, trace)
                    if sub_result.matched and sub_result.action != "return":
                        return sub_result
                    trace.append(f"  Returned from chain: {rule.jump_target}")
                    continue

                elif rule.action == "continue":
                    trace.append("  Action=continue, keep evaluating")
                    continue

                elif rule.action == "return":
                    return MatchResult(
                        matched=False,
                        action="return",
                        chain_name=chain.name,
                        chain_family=chain.family,
                        chain_hook=chain.hook,
                        rule_number=rule.number,
                        rule=rule,
                        trace=trace,
                    )

                else:
                    return MatchResult(
                        matched=True,
                        action=rule.action,
                        chain_name=chain.name,
                        chain_family=chain.family,
                        chain_hook=chain.hook,
                        rule_number=rule.number,
                        rule=rule,
                        trace=trace,
                    )
            else:
                trace.append(f"  Rule {rule.number}: no match")

        # No rule matched → default action
        trace.append(
            f"  No rule matched in {chain.name}, "
            f"applying default-action: {chain.default_action}"
        )

        return MatchResult(
            matched=True,
            action=chain.default_action,
            chain_name=chain.name,
            chain_family=chain.family,
            chain_hook=chain.hook,
            is_default_action=True,
            trace=trace,
        )

    def _rule_matches(
        self,
        rule: Rule,
        traffic: TrafficTuple,
        trace: list[str],  # pylint: disable=unused-argument
    ) -> bool:
        """Check if ALL criteria in a rule match the traffic tuple."""
        # Protocol
        if rule.protocol is not None:
            if traffic.protocol is None:
                return False
            if not protocol_matches(traffic.protocol, rule.protocol):
                return False

        # Inbound interface
        if not self._interface_matches(
            rule.inbound_interface, traffic.inbound_interface, "inbound"
        ):
            return False

        # Outbound interface
        if not self._interface_matches(
            rule.outbound_interface, traffic.outbound_interface, "outbound"
        ):
            return False

        # Source
        if not self._source_dest_matches(
            rule.source, traffic.source_ip, traffic.port, is_source=True
        ):
            return False

        # Destination
        if not self._source_dest_matches(
            rule.destination, traffic.destination_ip, traffic.port, is_source=False
        ):
            return False

        # State
        if rule.state:
            if traffic.state is None or traffic.state not in rule.state:
                return False

        return True

    def _interface_matches(
        self,
        rule_iface: InterfaceCriteria,
        traffic_iface: Optional[str],
        direction: str,  # pylint: disable=unused-argument
    ) -> bool:
        """Check if interface criterion is satisfied."""
        if rule_iface.name is None and rule_iface.group is None:
            return True

        if rule_iface.name is not None:
            if traffic_iface is None:
                return False
            if not interface_matches(traffic_iface, rule_iface.name):
                return False

        if rule_iface.group is not None:
            if traffic_iface is None:
                return False
            if not self._interface_group_matches(traffic_iface, rule_iface.group):
                return False

        return True

    def _interface_group_matches(self, iface: str, group_spec: str) -> bool:
        """Check if interface belongs to an interface-group."""
        negated = group_spec.startswith("!")
        group_name = group_spec[1:] if negated else group_spec

        group = self.config.get_group("interface", group_name)
        if group is None:
            return negated

        matched = any(interface_matches(iface, member) for member in group.members)
        return (not matched) if negated else matched

    def _source_dest_matches(
        self,
        match: SourceDestCriteria,
        ip: str,
        port: Optional[int],
        is_source: bool,
    ) -> bool:
        """Check source/destination match criteria."""
        if self._is_empty_match(match):
            return True

        # Address matching
        if match.address is not None:
            if not ip:
                return False
            if match.address_mask is not None:
                if not ip_matches_with_mask(ip, match.address, match.address_mask):
                    return False
            else:
                if not ip_matches(ip, match.address):
                    return False

        # FQDN matching
        if match.fqdn is not None:
            if not ip or ip.lower() != match.fqdn.lower():
                return False

        # Port matching (destination only by default)
        if match.port is not None and not is_source:
            if port is None:
                return False
            if not port_matches(port, match.port):
                return False

        # Address group
        if match.address_group is not None:
            if not ip:
                return False
            if not self._address_group_matches(ip, match.address_group, "address"):
                return False

        # Network group
        if match.network_group is not None:
            if not ip:
                return False
            if not self._address_group_matches(ip, match.network_group, "network"):
                return False

        # Port group (destination only)
        if match.port_group is not None and not is_source:
            if port is None:
                return False
            if not self._port_group_matches(port, match.port_group):
                return False

        # IPv6 groups
        if match.ipv6_address_group is not None:
            if not ip:
                return False
            if not self._address_group_matches(ip, match.ipv6_address_group, "ipv6-address"):
                return False

        if match.ipv6_network_group is not None:
            if not ip:
                return False
            if not self._address_group_matches(ip, match.ipv6_network_group, "ipv6-network"):
                return False

        return True

    @staticmethod
    def _is_empty_match(match: SourceDestCriteria) -> bool:
        """Return True if no match criteria are set."""
        return all(
            getattr(match, field) is None
            for field in (
                "address",
                "address_mask",
                "fqdn",
                "port",
                "mac_address",
                "address_group",
                "network_group",
                "port_group",
                "mac_group",
                "domain_group",
                "ipv6_address_group",
                "ipv6_network_group",
            )
        )

    def _address_group_matches(
        self, ip: str, group_name: str, group_type: str
    ) -> bool:
        """Check if IP matches any member of an address/network group."""
        negated = group_name.startswith("!")
        clean_name = group_name[1:] if negated else group_name

        group = self.config.get_group(group_type, clean_name)

        # Fallback to ipv6 variant if primary lookup failed
        if group is None and group_type in ("address", "network"):
            group = self.config.get_group(f"ipv6-{group_type}", clean_name)

        if group is None:
            return negated

        matched = any(ip_matches(ip, member) for member in group.members)
        return (not matched) if negated else matched

    def _port_group_matches(self, port: int, group_name: str) -> bool:
        """Check if port matches any member of a port group."""
        negated = group_name.startswith("!")
        clean_name = group_name[1:] if negated else group_name

        group = self.config.get_group("port", clean_name)
        if group is None:
            return negated

        matched = any(port_matches(port, member) for member in group.members)
        return (not matched) if negated else matched
