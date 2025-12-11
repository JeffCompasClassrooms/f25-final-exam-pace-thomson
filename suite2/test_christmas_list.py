import os
import pickle
import pytest
from christmas_list import ChristmasList



def describe_ChristmasList():
    def describe___init__():
        def it_creates_file_if_missing(tmp_path):
            db_path = tmp_path / "test_data.dat"
            assert not db_path.exists()

            db = ChristmasList(str(db_path))

            assert db_path.exists()
            # Verify empty persistent state via public API
            assert db.loadItems() == []

        def it_preserves_existing_file_contents(tmp_path):
            db_path = tmp_path / "test_data.dat"
            initial_data = [{"name": "Toy", "purchased": False}]
            # Pre-populate file to simulate existing database
            with open(db_path, "wb") as f:
                pickle.dump(initial_data, f)

            db = ChristmasList(str(db_path))

            assert db_path.exists()
            assert db.loadItems() == initial_data

    def describe_loadItems():
        def it_returns_empty_list_for_new_db(tmp_path):
            db_path = tmp_path / "empty.dat"
            db = ChristmasList(str(db_path))

            assert db.loadItems() == []

        def it_reads_prepopulated_data(tmp_path):
            db_path = tmp_path / "pre.dat"
            expected = [{"name": "Toy", "purchased": False}, {"name": "Ball", "purchased": False}]
            with open(db_path, "wb") as f:
                pickle.dump(expected, f)

            db = ChristmasList(str(db_path))
            assert db.loadItems() == expected

        def it_handles_strings_with_special_characters(tmp_path):
            # Test edge case: strings with special characters
            db_path = tmp_path / "special.dat"
            special_data = ["hello\nworld", "test\tvalue", "path/to/file", "unicode: Σ╜áσÑ╜"]
            with open(db_path, "wb") as f:
                pickle.dump(special_data, f)

            db = ChristmasList(str(db_path))
            assert db.loadItems() == special_data

        def it_handles_very_long_strings(tmp_path):
            # Test boundary case: very long individual strings
            db_path = tmp_path / "long_strings.dat"
            long_string = "x" * 10000  # 10KB string
            long_data = [long_string, "normal", long_string]
            with open(db_path, "wb") as f:
                pickle.dump(long_data, f)

            db = ChristmasList(str(db_path))
            assert db.loadItems() == long_data

    
    def describe_saveItems():
        def it_overwrites_existing_content(tmp_path):
            db_path = tmp_path / "db.dat"
            db = ChristmasList(str(db_path))

            first = [{"name": "Toy", "purchased": False}] 
            second = [{"name": "Ball", "purchased": False}]

            db.saveItems(first)
            db.saveItems(second)

            assert db.loadItems() == second

        def it_persists_across_reopen(tmp_path):
            db_path = tmp_path / "db.dat"
            db = ChristmasList(str(db_path))

            data = [{"name": "Toy", "purchased": False}, {"name": "Ball", "purchased": False}]
            db.saveItems(data)

            # Reopen a new instance and verify persistence
            db2 = ChristmasList(str(db_path))
            assert db2.loadItems() == data

        def it_handles_empty_list(tmp_path):
            # Test edge case: saving empty list
            db_path = tmp_path / "empty_list.dat"
            db = ChristmasList(str(db_path))

            db.saveItems([])
            assert db.loadItems() == []

    def describe_add():
        def it_appends_one_item(tmp_path):
            db_path = tmp_path / "append.dat"
            db = ChristmasList(str(db_path))

            db.saveItems([{"name": "Toy", "purchased": False}])
            db.add("Ball")

            assert db.loadItems() == [{"name": "Toy", "purchased": False}, {"name": "Ball", "purchased": False}]

        def it_appends_in_order_over_multiple_calls(tmp_path):
            db_path = tmp_path / "append_many.dat"
            db = ChristmasList(str(db_path))

            values = ["a", "b"]
            for value in values:
                db.add(value)

            expected = [
                {"name": "a", "purchased": False}, 
                {"name": "b", "purchased": False}
            ]

            assert db.loadItems() == expected

        def it_handles_empty_string(tmp_path):
            # Test edge case: appending empty string
            db_path = tmp_path / "empty_string.dat"
            db = ChristmasList(str(db_path))

            db.saveItems([{"name": "start", "purchased": False}])
            db.add("")
            db.add("end")

            expected = [
                {"name": "start", "purchased": False}, 
                {"name": "", "purchased": False}, 
                {"name": "end", "purchased": False}
            ]

            assert db.loadItems() == expected
    
    def describe_remove():

        def it_removes_one_item(tmp_path):
            db_path = tmp_path / "remove.dat"
            db = ChristmasList(str(db_path))

            db.saveItems([{"name": "Toy", "purchased": False}, {"name": "Ball", "purchased": False}])
            db.remove("Ball")

            assert db.loadItems() == [{"name": "Toy", "purchased": False}]

        def it_maintains_order_over_multiple_calls(tmp_path):
            db_path = tmp_path / "remove_many.dat"
            db = ChristmasList(str(db_path))
            og = [
                {"name": "Toy", "purchased": False}, 
                {"name": "Ball", "purchased": False},
                {"name": "a", "purchased": False}, 
                {"name": "b", "purchased": False}
            ]
            db.saveItems(og)

            values = ["Toy", "a"]
            for value in values:
                db.remove(value)

            expected = [
                {"name": "Ball", "purchased": False}, 
                {"name": "b", "purchased": False}
            ]

            assert db.loadItems() == expected

        def it_handles_nonexistant_item(tmp_path):
            db_path = tmp_path / "check_off.dat"
            db = ChristmasList(str(db_path))

            db.saveItems([{"name": "Toy", "purchased": False}, {"name": "Ball", "purchased": False}])
            db.remove("other")

            assert db.loadItems() == [{"name": "Toy", "purchased": False}, {"name": "Ball", "purchased": False}]


    def describe_check_off():

        def it_check_offs_one_item(tmp_path):
            db_path = tmp_path / "check_off.dat"
            db = ChristmasList(str(db_path))

            db.saveItems([{"name": "Toy", "purchased": False}, {"name": "Ball", "purchased": False}])
            db.check_off("Ball")

            assert db.loadItems() == [{"name": "Toy", "purchased": False}, {"name": "Ball", "purchased": True}]

        def it_maintains_order_over_multiple_calls(tmp_path):
            db_path = tmp_path / "check_off_many.dat"
            db = ChristmasList(str(db_path))
            og = [
                {"name": "Toy", "purchased": False}, 
                {"name": "Ball", "purchased": False},
                {"name": "a", "purchased": False}, 
                {"name": "b", "purchased": False}
            ]
            db.saveItems(og)

            values = ["Toy", "a"]
            for value in values:
                db.check_off(value)

            expected = [
                {"name": "Toy", "purchased": True}, 
                {"name": "Ball", "purchased": False},
                {"name": "a", "purchased": True}, 
                {"name": "b", "purchased": False}
            ]

            assert db.loadItems() == expected

        def it_handles_nonexistant_item(tmp_path):
            db_path = tmp_path / "check_off.dat"
            db = ChristmasList(str(db_path))

            db.saveItems([{"name": "Toy", "purchased": False}, {"name": "Ball", "purchased": False}])
            db.check_off("other")

            assert db.loadItems() == [{"name": "Toy", "purchased": False}, {"name": "Ball", "purchased": False}]


    def describe_print_list():

        def prints_one_correctly_not_purchased(tmp_path, capsys):
            db_path = tmp_path / "prints_one.dat"
            db = ChristmasList(str(db_path))
            db.saveItems([{"name": "Toy", "purchased": False}])
            db.print_list()
            captured = capsys.readouterr()
            expected = "[_] Toy\n"
            assert captured.out == expected

        def prints_one_correctly_is_purchased(tmp_path, capsys):
            db_path = tmp_path / "prints_one.dat"
            db = ChristmasList(str(db_path))
            db.saveItems([{"name": "Toy", "purchased": True}])
            db.print_list()
            captured = capsys.readouterr()
            expected = "[x] Toy\n"
            assert captured.out == expected

        def prints_multiple_correctly(tmp_path, capsys):
            db_path = tmp_path / "prints_one.dat"
            db = ChristmasList(str(db_path))
            items = [
                {"name": "Toy", "purchased": True}, 
                {"name": "Ball", "purchased": False},
                {"name": "a", "purchased": True}, 
                {"name": "b", "purchased": False}
            ]
            db.saveItems(items)
            db.print_list()
            captured = capsys.readouterr()
            expected = "[x] Toy\n[_] Ball\n[x] a\n[_] b\n"
            assert captured.out == expected
        
        def prints_with_empty_name(tmp_path, capsys):
            db_path = tmp_path / "prints_one.dat"
            db = ChristmasList(str(db_path))
            items = [
                {"name": "Toy", "purchased": True}, 
                {"name": "", "purchased": False},
                {"name": "", "purchased": True}, 
                {"name": "b", "purchased": False}
            ]
            db.saveItems(items)
            db.print_list()
            captured = capsys.readouterr()
            expected = "[x] Toy\n[_] \n[x] \n[_] b\n"
            assert captured.out == expected

        def prints_with_empty_list(tmp_path, capsys):
            db_path = tmp_path / "prints_one.dat"
            db = ChristmasList(str(db_path))
            db.saveItems([])
            db.print_list()
            captured = capsys.readouterr()
            expected = ""
            assert captured.out == expected
