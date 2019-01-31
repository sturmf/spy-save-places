"""Solve the spy game!"""
from itertools import repeat, product

# Questions
# IODA: When to make a step function private? What about the tests at that point?
# IODA: Should it not be allowed to extract functions from pure functions?

# Refactorings
# Don't use -1 as Marker, MAX_DISTANCE, or NO_AGENT_IN_SIGHT would be nicer



class SafetyFinder:
    """A class that contains everything we need to find the
    safest places in the city for Alex to hide out
    """

    def __init__(self):
        self.char_to_int = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
            'F': 5,
            'G': 6,
            'H': 7,
            'I': 8,
            'J': 9,
            'K': 10,
        }

        self.int_to_char = inv_map = {v: k for k, v in self.char_to_int.items()}


    def convert_coordinates(self, agents):
        """This method should take a list of alphanumeric coordinates (e.g. 'A6')
        and return an array of the coordinates converted to arrays with zero-indexing.
        For instance, 'A6' should become [0, 5]

        Arguments:
        agents -- a list-like object containing alphanumeric coordinates.

        Returns a list of coordinates in zero-indexed vector form.
        """
        return [self._agent_to_coordinates(agent) for agent in agents]

    def _agent_to_coordinates(self, agent):
        return [self.char_to_int[agent[0]], int(agent[1:]) - 1]

    def find_safe_spaces(self, agents):
        """This method will take an array with agent locations and find
        the safest places in the city for Alex to hang out.

        Arguments:
        agents -- a list-like object containing the map coordinates of agents.
            Each entry should be formatted in indexed vector form,
            e.g. [0, 5], [3, 7], etc.

        Returns a list of safe spaces in indexed vector form.
        """

        # generate initial locations
        spaces = self._generate_initial_spaces(10, 10)
        # apply each agent to all locations
        for agent in agents:
            # place agent
            spaces = self._place_agent(spaces, agent)
        # reduce to safe spaces
        safe_spaces = self._filter_to_safe_spaces(spaces)
        # convert
        return self._convert_to_list_of_spaces(safe_spaces)

        # Other Idea
        # convert_agents_to_distance_maps
        # collate_map_fields_to_minima
        # find_safest_distance
        # convert_safest_fields_to_coordinates

    def _generate_initial_spaces(self, x_length, y_length):
        coordinates = set(product(range(x_length), range(y_length)))
        return {(x,y, -1) for (x,y) in coordinates}

    def _place_agent(self, spaces, agent):
        updated_spaces = set()
        (x_agent, y_agent) = agent

        # for each space
        for space in spaces:
            (x_space, y_space, current_distance) = space
            # calc distance to agent
            distance_to_agent = abs(x_agent - x_space) + abs(y_agent - y_space)
            # update space with highest threat = lowest number
            updated_distance = distance_to_agent if current_distance == -1 else min(current_distance, distance_to_agent)
            updated_spaces.add((x_space, y_space, updated_distance))

        return updated_spaces

    def _filter_to_safe_spaces(self, spaces):
        (x, y, max_distance) = max(spaces, key=lambda x: x[2])
        safe_spaces = {space for space in spaces
                       if
                       space[2] == max_distance and
                       space[2] != 0
                       }
        return safe_spaces

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
        return [str(self.int_to_char[x]) + str(y + 1) for x, y in safe_spaces]

    def _remove_agents_outside_map(self, agents_coordinates):
        return [agent for agent in agents_coordinates if agent[0] <= 10 and agent[1] <= 10]