"""Streamlit entry point: run with python -m streamlit run app.py."""

from pathlib import Path

import streamlit as st

from mapguesser.data import load_countries
from mapguesser.game import new_game
from mapguesser.i18n import translate

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Map Guesser", page_icon="🌍", layout="centered")


@st.cache_data
def get_countries():
    return load_countries(ROOT / "data/countries.json", ROOT / "assets/maps")


try:
    countries = get_countries()
except (OSError, ValueError) as error:
    st.error(f"Could not load the quiz / 无法加载题库: {error}")
    st.stop()

with st.sidebar:
    language = st.selectbox(
        "Language / 语言",
        ["en", "zh"],
        format_func=lambda value: {"en": "English", "zh": "中文"}[value],
        key="language",
    )


def text(key, **values):
    return translate(key, language, **values)


def restart():
    st.session_state.game = new_game(countries, rounds=min(10, len(countries)))


if "game" not in st.session_state:
    restart()

game = st.session_state.game
by_id = {country.id: country for country in countries}
question = game.current_question
correct_country = by_id[question.correct_id]

with st.sidebar:
    st.divider()
    st.subheader(text("how_to_play"))
    st.write(text("instructions"))
    st.caption(text("language_hint"))
    st.button(text("restart"), key="restart", on_click=restart, width="stretch")
    st.divider()
    st.caption(text("dataset", count=len(countries)))
    st.markdown("[Natural Earth](https://www.naturalearthdata.com/)")

st.caption(text("eyebrow"))
st.title("Map Guesser")
st.write(text("intro"))

progress, score = st.columns([3, 1])
with progress:
    st.caption(text("completed", count=game.answered_count, total=game.total_rounds))
    st.progress(game.answered_count / game.total_rounds)
with score:
    st.metric(text("score"), f"{game.score} / {game.total_rounds}")

st.divider()
st.subheader(text("question", number=game.index + 1, total=game.total_rounds))

with st.container(border=True):
    _, map_column, _ = st.columns([1, 6, 1])
    with map_column:
        # Serve SVG contents so the image URL does not expose the answer's filename.
        st.image(correct_country.map_path.read_text(encoding="utf-8"), width="stretch")

st.caption(text("choose"))
for start in (0, 2):
    columns = st.columns(2)
    for column, country_id in zip(columns, question.option_ids[start : start + 2], strict=True):
        with column:
            st.button(
                by_id[country_id].label(language),
                key=f"answer_{country_id}",
                on_click=game.answer,
                args=(country_id,),
                disabled=game.answered,
                width="stretch",
            )

if game.answered:
    country_name = correct_country.label(language)
    if game.selected_id == question.correct_id:
        st.success(text("correct", name=country_name))
    else:
        st.error(text("incorrect", name=country_name))

    if game.finished:
        st.subheader(text("game_over"))
        st.write(text("final_score", score=game.score, total=game.total_rounds))
        st.button(text("play_again"), key="play_again", type="primary", on_click=restart)
    else:
        st.button(
            text("next_question"),
            key="next_question",
            type="primary",
            on_click=game.advance,
        )
