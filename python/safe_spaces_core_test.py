"""Run unittests for the ThoughtWorks spy game"""
import unittest

from safe_spaces_core import SafetyFinderCore

class SafetyFinderCoreTest_find_safe_spaces__Decompositions(unittest.TestCase):

    def test_generate_initial_map(self):
        self.assertEqual(SafetyFinderCore()._generate_city_locations(2, 2),
                         {(0, 0), (1, 1), (0, 1), (1, 0)})

        self.assertEqual(SafetyFinderCore()._generate_city_locations(1, 1),
                         {(0, 0)})

    def test_place_agent(self):
        self.assertEqual({(0, 0, 0)},
                         SafetyFinderCore()._append_minimal_distances_to_locations({(0, 0)}, [[0, 0]]))

        self.assertEqual({(0, 0, 0), (1, 1, 2), (0, 1, 1), (1, 0, 1)},
                         SafetyFinderCore()._append_minimal_distances_to_locations(
                                                                     {(0, 0), (1, 1), (0, 1), (1, 0)}, [[0, 0]]))

        self.assertEqual({(0, 0, 1), (1, 1, 1), (0, 1, 0), (1, 0, 2)},
                         SafetyFinderCore()._append_minimal_distances_to_locations(
                                                                     {(0, 0), (1, 1), (0, 1), (1, 0)}, [[0, 1]]))

    def test_reduce_to_safe_spaces(self):
        self.assertEqual({(1, 0, 2)},
                         SafetyFinderCore()._filter_to_safe_spaces({(0, 0, 1), (1, 1, 1), (0, 1, 0), (1, 0, 2)}))

        self.assertEqual({(1, 0, 1), (0, 1, 1)},
                         SafetyFinderCore()._filter_to_safe_spaces({(0, 0, 0), (1, 1, 0), (0, 1, 1), (1, 0, 1)}))

    def test_convert_to_list_of_lists(self):
        self.assertEqual(sorted([[1, 0], [0, 1]]),
                         sorted(SafetyFinderCore()._convert_to_list_of_spaces({(1, 0, 1), (0, 1, 1)})))

class SafetyFinderCoreTest_advice_for_alex__Decompositions(unittest.TestCase):

    def test_convert_to_list_of_strings(self):
        self.assertEqual(sorted(SafetyFinderCore()._convert_to_list_of_strings([[0, 9], [0, 7], [5, 0]])),
                         sorted(['A10', 'A8', 'F1']))

    def test__remove_agents_outside_map(self):
        agents = [[10, 10], [12, 1], [5, 13], [2, 3]]
        self.assertEqual(sorted(SafetyFinderCore()._remove_agents_outside_city(agents)),
                         sorted([[2, 3]]))



if __name__ == '__main__':
    unittest.main()
