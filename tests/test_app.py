from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


def test_app_loads_and_generates_pairings() -> None:
    app = AppTest.from_file(ROOT / "app.py", default_timeout=10).run()

    assert not app.exception
    assert app.title[0].value == "🍸 Smart Bar Pairing Assistant"
    assert len(app.button) == 1

    app.button[0].click().run()

    assert not app.exception
    assert len(app.metric) == 3
