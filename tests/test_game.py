import random

import pytest

from mapguesser.game import new_game


@pytest.mark.parametrize("seed", [0, 7, 42])
def test_game_has_ten_unique_maps_and_four_unambiguous_options(countries, seed):
    game = new_game(countries, rng=random.Random(seed))
    assert len(game.questions) == 10
    assert len({question.correct_id for question in game.questions}) == 10
    for question in game.questions:
        assert len(set(question.option_ids)) == 4
        assert question.correct_id in question.option_ids


def test_correct_answer_cannot_be_counted_twice(countries):
    game = new_game(countries)
    game.answer(game.current_question.correct_id)
    with pytest.raises(ValueError, match="already been answered"):
        game.answer(game.current_question.correct_id)
    assert game.score == 1
    assert game.answered_count == 1


def test_invalid_answer_and_skipping_do_not_change_state(countries):
    game = new_game(countries)
    with pytest.raises(ValueError, match="current options"):
        game.answer("not-an-option")
    with pytest.raises(ValueError, match="before continuing"):
        game.advance()
    assert game.score == game.index == game.answered_count == 0
    assert not game.answered


def test_mixed_answers_finish_exactly_once_and_restart_clears_state(countries):
    game = new_game(countries, rng=random.Random(42))
    for index in range(10):
        question = game.current_question
        answer = (
            question.correct_id
            if index % 2 == 0
            else next(option for option in question.option_ids if option != question.correct_id)
        )
        game.answer(answer)
        assert game.answered_count == index + 1
        if index < 9:
            assert not game.finished
            game.advance()
            assert not game.answered
    assert game.finished
    assert game.score == 5
    with pytest.raises(ValueError, match="complete"):
        game.advance()
    restarted = new_game(countries)
    assert restarted.score == restarted.index == restarted.answered_count == 0
    assert not restarted.finished


def test_small_catalog_can_use_all_four_maps(countries):
    game = new_game(countries[:4], rounds=4)
    assert len({question.correct_id for question in game.questions}) == 4


@pytest.mark.parametrize("rounds", [0, 166])
def test_invalid_round_count_is_rejected(countries, rounds):
    with pytest.raises(ValueError, match="rounds"):
        new_game(countries, rounds=rounds)
