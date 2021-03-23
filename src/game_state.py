
from __future__ import annotations
import copy
from joblib import Parallel, delayed
from mesa.time import RandomActivation
import multiprocessing as mp
import networkx as nx
from queue import SimpleQueue
from typing import *


class Location:
    """Represents the most specific level of a place, such as a store, bar, gym, building, field, etc."""
    # METHODS
    def __init__(self,
                name: str,
                parent: LocationGroup=None,
                locked: bool=false,
                capacity: int=None,
                entry_requirements: Iterable[Callable]=None,
                *args, **kwargs):
        """
        Instantiates a new location with a given name and other attributes.

        Args:
            name (str): The name of the Location.
            parent (LocationGroup, optional): Most immediate parent location group to attach to.
            locked (bool, optional): Whether to manually block player from entry or not. If True, player is blocked entry even when satisfying all
                entry requirements. Defaults to false.
            capacity (int, optional): Maximum number of agents, including player, allowed tro be at location simultaneously. Defaults to None.
            entry_requirements (Iterable[Callable], optional): Functions that each agent must satisfy to be allowed entry to location. This includes
                the player. Each element must be callable with the agent as the only parameter. Defaults to None.
        """
        if len(name) == 0:
            raise ValueError('name cannot be empty')
        elif parent is not None and name in [child.name for child in parent.children]:
            raise ValueError(f'parent already has child with the exact same name \'{name}\'')

        # Essential attributes
        self.name = name
        self.parent = parent
        self.locked = locked
        self.capacity = capacity
        self.entry_requirements = entry_requirements

        # Adds this as child from parent's perspective
        if self.parent is not None:
            self.parent.add_child(child=self)

        # Other custom attributes
        self.attributes = dict()
        for key, value in args:
            self.attributes[key] = value
        for key, value in kwargs.items():
            self.attributes[key] = value

    def __repr__(self):
        """
        Representation of the Location object.

        Returns:
            str: Detailed string representing Location object.
        """
        return f'<Location: name={self.name}, parent={self.parent.name}, locked={self.locked}, capacity={self.capacity}, \
                entry_requirements_size={len(self.entry_requirements)}, attributes_size={len(self.attributes)}>'

    def __str__(self):
        """
        String version of the Location object.

        Returns:
            str: The name of the Location object.
        """
        return self.name

class LocationGroup:
    """
    A collection of either other LocationGroup objects, only Location objects, or a combination of both. This is simply used to organize the
    game map into a tree. For example, a city may contain districts, which then contain squares, malls, and school zones that have specific
    buildings (Location objects).
    """
    # METHODS
    def __init__(self, name: str, parent: LocationGroup=None, children: Iterable[Union[Location, LocationGroup]]=None, *args, **kwargs):
        """
        Initializes organized group of Location and LocationGroup objects.

        Args:
            name (str): The name of the LocationGroup.
            parent (LocationGroup, optional): Most immediate parent location group to attach to. Defaults to None.
            children (Iterable[Union[Location, LocationGroup]], optional): All immediate children of LocationGroup. Defaults to None.
        """

        # Essential attributes
        self.name = name
        self.parent = parent
        self.children = set(children)

        # Other custom attributes
        self.attributes = dict()
        for key, value in args:
            self.attributes[key] = value
        for key, value in kwargs.items():
            self.attributes[key] = value

    def __repr__(self):
        """
        Representation of the LocationGroup object.

        Returns:
            str: Detailed string representing the LocationGroup object.
        """
        return f'<Location: name={self.name}, parent={self.parent.name}, children={[child.name for child in self.children]}, \
                attributes_size={len(self.attributes)}>'

    def __str__(self):
        """
        String version of the LocationGroup object.

        Returns:
            str: The name of the LocationGroup object.
        """
        return self.name

    # ACCESSORS
    @property
    def parent(self):
        """Gets parent

        Returns:
            LocationGroups: Parent
        """
        return self.parent

    @parent.setter
    def parent(self, new_parent: LocationGroup):
        """
        Sets new parent 

        Args:
            new_parent (LocationGroup): [description]
        """
        self.parent.del_child(child=self)
        self.parent = new_parent

    # MUTATORS
    def add_child(self, child: Union[Location, LocationGroup]):
        """
        Adds new child node.

        Args:
            child (Union[Location, LocationGroup]): Child to be added.

        Returns:
            None: None
        """
        self.children.add(child=child)

    def del_child(self, child: Union[Location, LocationGroup, str]):
        """
        Deletes child from children based on object or name.

        Args:
            child (Union[Location, LocationGroup, str]): Child to remove.

        Raises:
            ValueError: Child does not exist in children.

        Returns:
            None: None
        """
        child_to_delete = child
        if type(child_to_delete) == str: child_to_delete = self.children[]]p;][p][p][]

    @property
    def children(self):
        """
        Gets iterable of child nodes.

        Return:
            Iterable[Union[Location, LocationGroup]]: Child nodes.
        """
        return self.children

    @children.setter
    def children(self, new_children: Iterable[Union[Location, LocationGroup]]):
        """
        Sets new children.

        Args:
            new_children (Iterable[Union[Location, LocationGroup]]): Iterable of Location or LocationGroup objects to be new children.
        """
        for child in self.children:
            child.parent = None

        self.children = children

class Map:
    """Entire game map as a tree hierarchy of LocationGroup objects, ending with leaves as Location objects"""
    # METHODS
    def __init__(self,
                name: str,
                root: LocationGroup,
                edges: Iterable[Tuple[Union[Location, str], Union[Location, str]]] = None,
                *args, **kwargs):
        """
        Initializes game map.

        Args:
            root (LocationGroup): The topmost LocationGroup object in the tree, whose parent must be None.
            edges (Iterable[Tuple[Union[Location, str], Union[Location, str]]], optional): List of edges to connect pairs of Location objects.
        """
        # Essential attributes
        self.root = root

        # Gathering locations into a dict with KV format {name: Location} (leaves of map tree)
        self.locations = dict()
        self.location_groups = dict()

        bfs_queue = SimpleQueue()
        bfs_queue.put(self.root)
        while not bfs_queue.empty():
            loc = bfs_queue.get()  # Either a Location or LocationGroup
            if type(loc) == Location:
                self.locations += {loc.name: loc}
            else:
                self.location_groups += {loc.name: loc}
                for child in loc.children:
                    bfs_queue.put(child)

        # Setting up graph representation of game map
        self.map = nx.Graph()
        self.map.add_nodes_from(nodes_for_adding=list(self.locations.values()))

        # Adding edges
        if edges is not None:
            prepared_edges = list()
            for edge in edges:
                prep_edge = copy.deepcopy(x=edge)
                loc1, loc2 = prep_edge
                if type(loc1) == str: prep_edge[0] = self.locations[loc1]
                if type(loc2) == str: prep_edge[1] = self.locations[loc2]
                prepared_edges.append(prep_edge)
            self.map.add_edges_from(ebunch_to_add=prepared_edges)

        # Other custom attributes
        self.attributes = dict()
        for key, value in args:
            self.attributes[key] = value
        for key, value in kwargs.items():
            self.attributes[key] = value

    def __repr__(self):
        """
        Representation of the Map object.

        Returns:
            str: Detailed string representing the Map object.
        """
        return f'<Location: name={self.name}, root={self.root.name}, attributes_size={len(self.attributes)}}>'

    def __str__(self):
        """
        String version of the Map object.

        Returns:
            str: The name of the Map object.
        """
        return self.name

    def __contains__(self, item: Union[Location, LocationGroup, str]):
        """
        Checks whether a Location or LocationGroup exists in the game map. This can also be referenced by the name.

        Args:
            item (Union[Location, LocationGroup, str]): Item to check for existence in the game map.
        """
        if type(item) == str:
            if __debug__:
                print('Map - __contains__ - item is str')
            return item in self.locations or item in self.location_groups
        elif type(item) == Location:
            if __debug__:
                print('Map - __contains__ - item is Location')
            return item in list(self.locations.values())
        if __debug__:
                print('Map - __contains__ - item is LocationGroup')
        return item in list(self.location_groups.values())

    # ACCESSORS
    def get_locations(self, name: bool=False):
        """
        Get all Location objects in the game map. If `name=True`, then only a list of names (str) is returned.

        Args:
            name (bool, optional): If True, only names are returned. Defaults to False.
        """
        if name:
            return list(self.locations.keys())
        return list(self.locations.values())

    def get_location_groups(self, name: bool=False):
        """
        Get all LocationGroup objects in the game map. If `name=True`, then only a list of names (str) is returned.

        Args:
            name (bool, optional): If True, only names are returned. Defaults to False.
        """
        if name:
            return list(self.location_groups.keys())
        return list(self.location_groups.values())

