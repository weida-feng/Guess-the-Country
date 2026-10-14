from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_language_switch_preserves_question_answers_and_score():
    app = AppTest.from_file(str(APP), default_timeout=10).run()
    assert not app.exception
    assert app.selectbox(key="language").value == "en"
    game = app.session_state["game"]
    question = game.current_question
    app.button(key=f"answer_{question.correct_id}").click().run()
    assert app.session_state["game"].score == 1

    app.selectbox(key="language").set_value("zh").run()
    assert not app.exception
    assert app.session_state["game"].current_question == question
    assert app.session_state["game"].score == 1
    assert app.success[0].value.startswith("答对了")
    assert all(button.disabled for button in app.button if button.key.startswith("answer_"))

    app.button(key="next_question").click().run()
    assert app.session_state["game"].index == 1
    question = app.session_state["game"].current_question
    app.selectbox(key="language").set_value("en").run()
    assert app.session_state["game"].current_question == question
    app.button(key="restart").click().run()
    assert app.session_state["game"].score == 0
    assert app.session_state["game"].answered_count == 0


def test_complete_ten_rounds_then_play_again():
    app = AppTest.from_file(str(APP), default_timeout=10).run()
    seen = set()
    for index in range(10):
        question = app.session_state["game"].current_question
        assert question.correct_id not in seen
        seen.add(question.correct_id)
        app.button(key=f"answer_{question.correct_id}").click().run()
        assert not app.exception
        if index < 9:
            app.button(key="next_question").click().run()
    assert app.session_state["game"].finished
    assert app.session_state["game"].score == 10
    assert len([header for header in app.subheader if header.value == "Game complete"]) == 1
    app.selectbox(key="language").set_value("zh").run()
    assert app.session_state["game"].score == 10
    assert app.button(key="play_again").label == "再玩一次"
    app.button(key="play_again").click().run()
    assert not app.exception
    assert app.session_state["game"].answered_count == 0
    assert app.session_state["game"].score == 0
    assert app.selectbox(key="language").value == "zh"


def test_app_can_start_outside_project_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    app = AppTest.from_file(str(APP), default_timeout=10).run()
    assert not app.exception
    assert app.title[0].value == "Map Guesser"
