import pytest
from brute import Brute
from unittest.mock import Mock, patch
import hashlib
import time

@pytest.fixture
def brute():
    return Brute("po")

def describe_brute():

    def describe_init():

        def init_creates_brute(brute):
            assert isinstance(brute, Brute)

        def init_sets_target_and_hashes_it(brute):
            target = hashlib.sha512(bytes("po", "utf-8")).hexdigest()
            assert target == brute.target

    def describe_hash():

        def hash_correctly_hashes(brute):
            target = hashlib.sha512(bytes("po", "utf-8")).hexdigest()
            assert target == brute.hash("po")

        def hash_isnt_same(brute):
            target = hashlib.sha512(bytes("po", "utf-8")).hexdigest()
            assert target != "po"

        def hashes_empty_string(brute):
            expected = hashlib.sha512(bytes("", "utf-8")).hexdigest()
            assert brute.hash("") == expected

    def describe_randomGuess():
        def randomGuess_is_between_1_and_8_chars(brute):
            for i in range(10):
                s = brute.randomGuess()
                assert len(s) >= 1 and len(s) <= 8
            
        def randomGuess_returns_arent_same(brute):
            guesses = []
            for i in range(10):
                s = brute.randomGuess()
                assert s not in guesses
                guesses.append(s)

        def randomGuess_returns_are_alphanum(brute):
            guesses = []
            for i in range(10):
                s = brute.randomGuess()
                assert s.isalnum()

        

    def describe_bruteOnce():

        def works_with_same_pass(brute):
            assert brute.bruteOnce("po") is True
        
        def works_with_wrong_pass(brute):
            assert brute.bruteOnce("not") is False

    def describe_bruteMany():

        def it_correctly_breaks_pass(mocker, brute):
            mock_random_guess = mocker.patch.object(brute, "randomGuess", return_value="po")
            assert brute.bruteMany() is not -1
            mock_random_guess.assert_called_once_with()

        def it_doesnt_breaks_pass_with_wrong_random(mocker, brute):
            mock_random_guess = mocker.patch.object(brute, "randomGuess", return_value="NOT")
            assert brute.bruteMany(limit=10) is -1

        def respects_limit_no_calls_when_zero(brute, mocker):
            mocker.patch.object(brute, "randomGuess")
            brute.bruteMany(limit=0)
            brute.randomGuess.assert_not_called()
        
        def calls_randomGuess_exact_limit(brute, mocker):
            mock_rg = mocker.patch.object(brute, "randomGuess", return_value="NO_MATCH")
            brute.bruteMany(limit=5)
            assert mock_rg.call_count == 5

        def correctly_times_guess_approximately(mocker, brute):
            # mock_random_guess = mocker.patch.object(brute, "randomGuess", return_value="po")
            t1 = time.time()
            answer = brute.bruteMany()
            total_time = time.time() - t1
            # checks for how close they are, need to be in a tenth of a second
            assert abs(total_time - answer) <= 0.1 
            





        



   


