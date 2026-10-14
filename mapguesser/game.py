"""Quiz state uses country IDs, independently of the selected UI language."""

import random
from collections.abc import Sequence
from dataclasses import dataclass

from mapguesser.data import Country


@dataclass(frozen=True)
class Question:
    correct_id: str
    option_ids: tuple[str, ...]


@dataclass
class Game:
    questions: tuple[Question, ...]
    index: int = 0
    score: int = 0
    selected_id: str | None = None

    @property
    def current_question(self) -> Question:
        return self.questions[self.index]

    @property
    def total_rounds(self) -> int:
        return len(self.questions)

    @property
    def answered(self) -> bool:
        return self.selected_id is not None

    @property
    def answered_count(self) -> int:
        return self.index + int(self.answered)

    @property
    def finished(self) -> bool:
        return self.answered and self.index == self.total_rounds - 1

    def answer(self, country_id: str) -> None:
        if self.answered:
            raise ValueError("This question has already been answered.")
        if country_id not in self.current_question.option_ids:
            raise ValueError("The answer must be one of the current options.")
        self.selected_id = country_id
        self.score += int(country_id == self.current_question.correct_id)

    def advance(self) -> None:
        if not self.answered:
            raise ValueError("Answer the current question before continuing.")
        if self.finished:
            raise ValueError("The game is complete; start a new game.")
        self.index += 1
        self.selected_id = None


def new_game(
    countries: Sequence[Country], rounds: int = 10, rng: random.Random | None = None
) -> Game:
    ids = [country.id for country in countries]
    if len(set(ids)) != len(ids) or len(ids) < 4:
        raise ValueError("A game requires at least four distinct countries.")
    if not 1 <= rounds <= len(ids):
        raise ValueError("The number of rounds must fit the country catalog.")
    rng = rng if rng is not None else random.Random()
    questions = []
    for correct_id in rng.sample(ids, rounds):
        options = rng.sample([identifier for identifier in ids if identifier != correct_id], 3)
        options.append(correct_id)
        rng.shuffle(options)
        questions.append(Question(correct_id, tuple(options)))
    return Game(tuple(questions))
