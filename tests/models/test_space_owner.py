import pytest

from src.models.space_owner import SpaceOwner


class TestSpaceOwner(object):
    def test_insert(self, space_owner_data_with_spaces, another_space_demo):
        space_owner = SpaceOwner()
        space_owner.add_from_dict(space_owner_data_with_spaces)
        space_owner.spaces.append(another_space_demo)
        space_owner.insert()
        assert space_owner.id > 0
        assert space_owner.name == space_owner_data_with_spaces.get("name")
        assert space_owner.email == space_owner_data_with_spaces.get("email")
        assert len(space_owner.spaces) == 2

    def test_delete(self, insert_space_owner_with_spaces):
        insert_space_owner_with_spaces.delete()
        assert (
            SpaceOwner.list(
                criteria=[SpaceOwner.id == insert_space_owner_with_spaces.id]
            )[1]
            == 0
        )  # Checks if the lenght of the returning list is equal to 0 if len==0 ==> AssertionError
