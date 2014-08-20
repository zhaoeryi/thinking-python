import pkg_resources
import testtools
from thinking.tests import base


class EntrypointTestCase(base.ThinkingTestCase):
        @testtools.skip
        def test_load_entry_point_with_require(self):
            # __requires__ = 'testegg==0.1.0'
            console_func = pkg_resources.load_entry_point("testegg", "console_scripts", "testegg_entry")
            console_func()

            entry_act = pkg_resources.load_entry_point("testegg", "entry_actions", "entry_act_add")
            entry_act()

        @testtools.skip
        def test_load_entry_point(self):
            console_func = pkg_resources.load_entry_point("testegg", "console_scripts", "testegg_entry")
            console_func()

            entry_act = pkg_resources.load_entry_point("testegg", "entry_actions", "entry_act_add")
            entry_act()

        @testtools.skip
        def test_iter_entry_points(self):
            for entrypoint in pkg_resources.iter_entry_points("console_scripts", "testegg_entry"):
                    plugin = entrypoint.load()
                    plugin()

            for entrypoint in pkg_resources.iter_entry_points("entry_actions"):
                    plugin = entrypoint.load()
                    plugin()
