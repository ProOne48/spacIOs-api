import pytest

from src.models.space_owner import SpaceOwner
from src.models.space import Space


class TestSpace(object):
    def test_insert(self, space_data, insert_space_owner):
        space = Space()
        space.add_from_dict(space_data)
        assert len(insert_space_owner.spaces) == 0
        space.insert()
        assert space.id > 0
        assert space.name == space_data.get('name')
        assert space.max_capacity == space_data.get('max_capacity')
        assert space.space_owner_id == space_data.get('space_owner_id')
        assert len(insert_space_owner.spaces) == 1

    def test_delete(self, insert_space_owner, insert_space):
        insert_space.delete()
        assert (
            Space.list(criteria=[Space.id == insert_space.id])[1] == 0
        )
