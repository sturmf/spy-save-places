"""Solve the spy game!"""
from itertools import repeat, product

# Questions
# IODA: When to make a step function private? What about the tests at that point?
# IODA: Should it not be allowed to extract functions from pure functions?
# IODA: When to introduce classes?
# IODA: When to crefactory primitive types to explicit data types?
# IODA: Thoughts on early returns? Usually an if statement and a return statement - IODA violation?

# Refactorings
# Introduce space data type with coordinates and min distance
# Don't use -1 as Marker, MAX_DISTANCE, or NO_AGENT_IN_SIGHT would be nicer
# Pull all occurences of map size information out of methods to a single place
# Add test for spies on the map edge to catch +-1 errors
# Correct expected actual ordering in assert calls
# Switch to iterator objects

# find save spaces
#
# Second Idea
# generate initial locations
# apply each agent to all locations
# reduce to safe spaces
# convert to response model
#
# First Idea
# convert_agents_to_distance_maps
# collate_map_fields_to_minima
# find_safest_distance
# convert_safest_fields_to_coordinates

class SafetyFinder:
    """A class that contains everything we need to find the
    safest places in the city for Alex to hide out
    """

    def __init__(self, city_rows=10, city_columns=10):
        self.city_rows = city_rows
        self.city_columns = city_columns

    def convert_coordinates(self, agents):
        """This method should take a list of alphanumeric coordinates (e.g. 'A6')
        and return an array of the coordinates converted to arrays with zero-indexing.
        For instance, 'A6' should become [0, 5]

        Arguments:
        agents -- a list-like object containing alphanumeric coordinates.

        Returns a list of coordinates in zero-indexed vector form.
        """
        return list(map(self._agent_to_coordinates, agents))

    def _agent_to_coordinates(self, agent):
        return [ord(agent[0])-ord("A"), int(agent[1:])-1]

    def find_safe_spaces(self, agents):
        """This method will take an array with agent locations and find
        the safest places in the city for Alex to hang out.

        Arguments:
        agents -- a list-like object containing the map coordinates of agents.
            Each entry should be formatted in indexed vector form,
            e.g. [0, 5], [3, 7], etc.

        Returns a list of safe spaces in indexed vector form.
        """
        initial_spaces = self._generate_initial_spaces(self.city_columns, self.city_rows)
        spaces_with_minimal_distances = self._calculate_minimal_distances(initial_spaces, agents)
        safe_spaces = self._filter_to_safe_spaces(spaces_with_minimal_distances)

        return self._convert_to_list_of_spaces(safe_spaces)

    def _generate_initial_spaces(self, x_length, y_length):
        coordinates = set(product(range(x_length), range(y_length)))
        return coordinates

    def _calculate_minimal_distances(self, spaces, agents):
        updated_spaces = set()
        for space in spaces:
            distances = [abs(agent[0] - space[0]) + abs(agent[1] - space[1]) for agent in agents]
            updated_spaces.add((space[0], space[1], min(distances)))
        return updated_spaces

    def _filter_to_safe_spaces(self, spaces):
        (x, y, max_distance) = max(spaces, key=lambda s: s[2])

        if max_distance == 0:
            return set()

        return set(filter(lambda s: s[2] == max_distance, spaces))

    def _convert_to_list_of_spaces(self, spaces):
        return [[x, y] for (x , y, d) in spaces]

    def advice_for_alex(self, agents):
        """This method will take an array with agent locations and offer advice
        to Alex for where she should hide out in the city, with special advice for
        edge cases.

        Arguments:
        agents -- a list-like object containing the map coordinates of the agents.
            Each entry should be formatted in alphanumeric form, e.g. A10, E6, etc.

        Returns either a list of alphanumeric map coordinates for Alex to hide in,
        or a specialized message informing her of edge cases
        """
        agents_coordinates = self.convert_coordinates(agents)
        agents_coordinates = self._remove_agents_outside_map(agents_coordinates)

        if len(agents_coordinates) == 0:
            return 'The whole city is safe for Alex! :-)'

        safe_spaces = self.find_safe_spaces(agents_coordinates)

        if len(safe_spaces) == 0:
            return 'There are no safe locations for Alex! :-('

        return self._convert_to_list_of_strings(safe_spaces)

    def _convert_to_list_of_strings(self, safe_spaces):
        return [chr(x + ord("A")) + str(y + 1) for x, y in safe_spaces]

    def _remove_agents_outside_map(self, agents_coordinates):
        return [agent for agent in agents_coordinates if agent[0] < 10 and agent[1] < 10]

