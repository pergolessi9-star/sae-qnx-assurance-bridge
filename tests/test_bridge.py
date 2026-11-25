import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "bridge", Path(__file__).parents[1] / "sae_qnx_assurance.py"
)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class BridgeTests(unittest.TestCase):
    def test_target_mapping(self):
        self.assertEqual(bridge.TARGETS["aarch64"], "gcc_ntoaarch64le")
        self.assertEqual(bridge.TARGETS["x86_64"], "gcc_ntox86_64")

    def test_sha256(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.txt"
            path.write_text("abc", encoding="utf-8")
            self.assertEqual(
                bridge.sha256(path),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )

    def test_elf_machine(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "probe.elf"
            header = bytearray(20)
            header[:4] = bytes([127, 69, 76, 70])
            header[4] = 2
            header[5] = 1
            header[18:20] = (183).to_bytes(2, "little")
            path.write_bytes(header)
            self.assertEqual(bridge.elf_machine(path), 183)

    def test_stage_source_copies_from_unicode_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_dir = root / "origen_con_acentos"
            stage_dir = root / "staging_ascii"
            source_dir.mkdir()
            source = source_dir / "prueba_ñ.c"
            source.write_text("int main(void) { return 0; }", encoding="utf-8")
            staged = bridge.stage_source(source, stage_dir)
            self.assertEqual(staged.name, "sae_qnx_probe.c")
            self.assertEqual(staged.read_bytes(), source.read_bytes())
            self.assertEqual(bridge.sha256(staged), bridge.sha256(source))

    def test_sdk_inspection_is_explicit(self):
        self.assertIn(
            bridge.inspect_sdk()["status"], {"BLOCKED", "READY_FOR_BUILD"}
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
