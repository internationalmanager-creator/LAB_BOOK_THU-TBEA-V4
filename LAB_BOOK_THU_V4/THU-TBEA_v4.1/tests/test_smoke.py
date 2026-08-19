# tests/test_smoke.py - prueba rapida de importacion y constantes
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import constants  # noqa: E402


def test_constantes():
    assert abs(constants.phi - 1.6180339887) < 1e-9
    assert constants.H0_ref == 76.0
    assert 0 < constants.xi_shield < 1


if __name__ == '__main__':
    test_constantes()
    print('test_smoke OK')
