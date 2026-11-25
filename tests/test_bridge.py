import importlib.util, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("bridge",Path(__file__).parents[1]/"sae_qnx_assurance.py")
bridge=importlib.util.module_from_spec(spec); spec.loader.exec_module(bridge)
class BridgeTests(unittest.TestCase):
    def test_target_mapping(self):
        self.assertEqual(bridge.TARGETS["aarch64"],"gcc_ntoaarch64le")
    def test_sha256(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x"; p.write_text("abc")
            self.assertEqual(bridge.sha256(p),"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
    def test_sdk_inspection_is_explicit(self):
        self.assertIn(bridge.inspect_sdk()["status"],{"BLOCKED","READY_FOR_BUILD"})
if __name__=="__main__": unittest.main(verbosity=2)
