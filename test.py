import pytest

import bin_to_ifd


@pytest.fixture()
def mim_tags():
    path = "./ifd_tags_in_mim.txt"
    with open(path) as f:
        tags = set()
        for line in f:
            tags.update(line.strip().split())
    return tags


def test_öll_mörk(mim_tags):
    legal_ifd_tags = bin_to_ifd.öll_mörk(strip=True)
    mim_only_tags = mim_tags - legal_ifd_tags
    assert mim_only_tags == {"nheo-ö", "nvee-ö"}, "These are incorrect tags in MÍM"
    # Þetta er örggulega of mikið.
    assert len(legal_ifd_tags) == 705
