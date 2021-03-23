import pytest

import bin_to_ifd
from bin_to_ifd import (
    ao_mörk,
    fn_mörk,
    gr_mörk,
    greinar_mörk,
    lo_mörk,
    no_mörk,
    sk_mörk,
    so_mörk,
    st_mörk,
    to_mörk,
)


@pytest.fixture()
def mim_tags():
    path = "./ifd_tags_in_mim.txt"
    with open(path) as f:
        tags = set()
        for line in f:
            tags.update(line.strip().split())
    return tags


def test_öll_mörk_lengd():
    def all_len(mörk, lengd: int):
        return all(len(mark) == lengd for mark in mörk)

    assert all_len(no_mörk(), 6)
    assert all_len(lo_mörk(), 6)
    assert all_len(fn_mörk(), 5)
    assert all_len(gr_mörk(), 4)
    assert all_len(to_mörk(), 5)
    assert all_len(so_mörk(), 6)
    assert all_len(ao_mörk(), 3)
    assert all_len(st_mörk(), 2)
    assert all_len(greinar_mörk(), 2)
    assert all_len(sk_mörk(), 2)


def test_öll_mörk(mim_tags):
    legal_ifd_tags = bin_to_ifd.öll_mörk(strip=True)
    mim_only_tags = mim_tags - legal_ifd_tags
    assert mim_only_tags == {"nheo-ö", "nvee-ö"}, "These are incorrect tags in MÍM"
    # Þetta er örggulega of mikið.
    assert len(legal_ifd_tags) == 705


def test_parsing():
    BIN_LOCATION = "/home/haukurpj/Resources/Data/DIM/DIM_2020.06_SHsnid.csv"
    legal_ifd_tags = bin_to_ifd.öll_mörk(strip=True)
    legal_ifd_tags.add("fp")
    with open(BIN_LOCATION) as f:
        for line in f:
            lemma, auðkenni, kyn_orðflokkur, hluti, orðmynd, mörk = line.strip().split(
                ";"
            )
            mim_mark = bin_to_ifd.parse_bin_str(
                orðmynd=orðmynd,
                lemma=lemma,
                kyn_orðflokkur=kyn_orðflokkur,
                mörk=mörk,
                samtengingar="c",
                afturbeygð_fn="fp",
            )
            # Samtengingar og afturbeygð fornöfn e
            if mim_mark is None:
                continue
            assert mim_mark in legal_ifd_tags, f"Röng þýðing: {line=} -> {mim_mark=}"
