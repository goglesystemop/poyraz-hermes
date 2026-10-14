"""Consumer regressions against the actual Hermes driver adapter, no UI input."""
import unittest
from tools.computer_use.cua_backend import CuaDriverBackend


class StrictSession:
    def __init__(self, legacy=False):
        self.legacy = legacy
        self.calls = []
        self.capabilities_discovered = True

    def supports_input_property(self, tool, name):
        return name == 'element_token' or (name == 'element_index' and self.legacy)

    def supports_capability(self, *args, **kwargs):
        return False

    def call_tool(self, tool, args):
        self.calls.append(dict(args))
        if not self.legacy and 'element_index' in args:
            return {'data': {'message': 'Unknown property element_index'},
                    'structuredContent': {}, 'isError': True}
        return {'data': {}, 'structuredContent': {'effect': 'confirmed'}, 'isError': False}


class DriverCompatibilityTests(unittest.TestCase):
    def test_tokenless_index_is_refused_before_driver_and_requests_a_fresh_pixel_observation(self):
        backend = CuaDriverBackend.__new__(CuaDriverBackend)
        backend._session = StrictSession()
        backend._session_id = 'owned-fixture'
        backend._snapshot_tokens = {}
        result = backend._action('click', {'element_index': 4})
        self.assertFalse(result.ok)
        self.assertEqual(result.code, 'element_reference_unavailable')
        self.assertEqual(result.escalation['recommended'], 'px')
        self.assertEqual(backend._session.calls, [])

    def test_modern_token_schema_accepts_the_observed_identity_without_legacy_property(self):
        backend = CuaDriverBackend.__new__(CuaDriverBackend)
        backend._session = StrictSession()
        backend._session_id = 'owned-fixture'
        backend._snapshot_tokens = {4: 'fresh-observation-token'}
        result = backend._action('click', {'element_index': 4, 'pid': 789, 'window_id': 123})
        self.assertTrue(result.ok)
        payload = backend._session.calls[0]
        self.assertEqual(payload['element_token'], 'fresh-observation-token')
        self.assertNotIn('element_index', payload)
        self.assertEqual(payload['window_id'], 123)

    def test_legacy_schema_still_receives_its_supported_index_and_same_token(self):
        backend = CuaDriverBackend.__new__(CuaDriverBackend)
        backend._session = StrictSession(legacy=True)
        backend._session_id = 'owned-fixture'
        backend._snapshot_tokens = {4: 'fresh-observation-token'}
        self.assertTrue(backend._action('click', {'element_index': 4}).ok)
        self.assertEqual(backend._session.calls[0]['element_index'], 4)
        self.assertEqual(backend._session.calls[0]['element_token'], 'fresh-observation-token')


if __name__ == '__main__':
    unittest.main()
