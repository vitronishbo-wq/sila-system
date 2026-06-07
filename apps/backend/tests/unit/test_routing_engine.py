from apps.backend.app.modules.justice.civil_registry.application.services.routing_engine import (
    RequestState,
    RoutingRule,
)


class TestRoutingStates:
    def test_initial_states(self):
        states = RequestState.initial_states()
        assert RequestState.EM_ANALISE_COMUNAL in states
        assert len(states) == 4

    def test_terminal_states(self):
        states = RequestState.terminal_states()
        assert RequestState.RESOLVIDO in states
        assert len(states) == 3

    def test_waiting_states(self):
        states = RequestState.waiting_states()
        assert len(states) == 3


class TestRoutingRules:
    def test_routing_rules_exist(self):
        assert hasattr(RoutingRule, "COMUNA_ONLY")
        assert hasattr(RoutingRule, "MUNICIPIO_ONLY")
        assert hasattr(RoutingRule, "PROVINCIA_ONLY")
        assert hasattr(RoutingRule, "COMUNA_ESCALABLE")
        assert hasattr(RoutingRule, "MUNICIPIO_ESCALABLE")


class TestStateTransitions:
    def test_no_overlap_initial_and_terminal(self):
        initial = set(RequestState.initial_states())
        terminal = set(RequestState.terminal_states())
        assert len(initial & terminal) == 0
