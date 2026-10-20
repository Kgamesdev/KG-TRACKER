import subprocess
import sys
import threading
import unittest
import uuid
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QEventLoop, QTimer

from core.single_instance import SingleInstance


class SingleInstanceTests(unittest.TestCase):
    def test_seven_launches_keep_one_primary_and_request_activation(self):
        app = QCoreApplication.instance() or QCoreApplication([])
        name = f"kg_tracker_test_{uuid.uuid4().hex}"
        primary = SingleInstance(name)
        self.assertTrue(primary.is_primary)

        loop = QEventLoop()
        requested = []
        primary.activation_requested.connect(
            lambda: requested.append(True)
        )
        timeout = QTimer()
        timeout.setSingleShot(True)
        timeout.timeout.connect(loop.quit)
        timeout.start(5000)
        worker_finished = threading.Event()
        poll_worker = QTimer()
        poll_worker.setInterval(20)
        poll_worker.timeout.connect(
            lambda: loop.quit() if worker_finished.is_set() else None
        )
        poll_worker.start()

        project_dir = Path(__file__).resolve().parents[1]
        child_code = (
            "from core.single_instance import SingleInstance; "
            f"manager = SingleInstance({name!r}); "
            "print('primary' if manager.is_primary else 'secondary')"
        )
        child_results = []

        def launch_six_more():
            try:
                for _ in range(6):
                    result = subprocess.run(
                        [sys.executable, "-c", child_code],
                        cwd=project_dir,
                        capture_output=True,
                        text=True,
                        timeout=5,
                    )
                    child_results.append((result.returncode, result.stdout.strip(), result.stderr))
            finally:
                worker_finished.set()

        launcher = threading.Thread(target=launch_six_more, daemon=True)

        try:
            launcher.start()
            loop.exec()
            launcher.join(timeout=5)
            self.assertFalse(launcher.is_alive(), "Las aperturas secundarias se bloquearon")
            self.assertEqual(len(child_results), 6)
            self.assertTrue(all(code == 0 for code, _, _ in child_results))
            self.assertTrue(all(result == "secondary" for _, result, _ in child_results))
            self.assertEqual(len(requested), 6)
        finally:
            timeout.stop()
            poll_worker.stop()
            primary.close()


if __name__ == "__main__":
    unittest.main()
