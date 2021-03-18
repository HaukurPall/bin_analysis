import re
from typing import Optional


def read_legal_ifd(path: str) -> set[str]:
    with open(path) as f:
        tags = set()
        for line in f:
            tags.update(line.strip().split())
    return tags


legal_ifd_tags = read_legal_ifd("./legal_ifd_tags.txt")


def kyn(mork: str) -> str:
    if "KVK" in mork:
        return "v"
    if "KK" in mork:
        return "k"
    if "HK" in mork:
        return "h"
    return ""


def tala(mork: str) -> str:
    if "FT" in mork:
        return "f"
    if "ET" in mork:
        return "e"
    return ""


def fall(mork: str) -> str:
    if "NF" in mork:
        return "n"
    if "ÞF" in mork:
        return "o"
    if "ÞGF" in mork:
        return "þ"
    if "EF" in mork:
        return "e"
    return ""


def beyging(mork: str) -> str:
    if "SB" in mork:
        return "s"
    if "VB" in mork:
        return "v"
    return "svó"


frumstig = re.compile(r"F(ST|SB|VB)")
miðstig = re.compile(r"M(ST|SB|VB)")
efstastig = re.compile(r"E(ST|SB|VB)")


def stig(mork: str) -> str:
    if frumstig.search(mork) is not None:
        return "f"
    if miðstig.search(mork) is not None:
        return "m"
    if efstastig.search(mork) is not None:
        return "e"
    return ""


def pers(mork: str) -> str:
    if "1P" in mork:
        return "1"
    if "2P" in mork:
        return "2"
    if "3P" in mork:
        return "3"
    return ""


def háttur(mork: str) -> str:
    if "LHNT" in mork:
        return "l"
    if "LHÞT" in mork:
        return "þ"
    if "BH" in mork:
        return "b"
    if "NH" in mork:
        return "n"
    if "OSKH" in mork:
        # Skilgreint í BÍN en ónotað
        raise ValueError("Óskháttur er ekki studdur")
    if "VH" in mork:
        return "v"
    if "FH" in mork:
        return "f"
    return ""


def mynd(mork: str) -> str:
    if "GM" in mork:
        return "g"
    if "MM" in mork:
        return "m"
    return ""


def tíð(mork: str) -> str:
    if "NT" in mork:
        return "n"
    if "ÞT" in mork:
        return "þ"
    return ""


def greinir(mork: str) -> str:
    if "gr" in mork:
        return "g"
    return ""


def sérnafn(orðmynd: str) -> str:
    if orðmynd.islower():
        return ""
    return "s"


def pfn_kyn(lemma: str) -> str:
    if lemma in {"ég", "þér", "vér", "þú"}:
        # Ekkert kyn
        return ""
    elif lemma == "hann":
        return "k"
    elif lemma == "hún":
        return "v"
    elif lemma == "það":
        return "h"
    else:
        raise ValueError(f"Unknown {lemma=}")


def pfn_persóna(lemma: str) -> str:
    if lemma in {"ég", "vér"}:
        return "1"
    elif lemma in {"þér", "þú"}:
        return "2"
    else:
        # Upplýsingum um 3.P er sleppt
        return ""


def rt_beyging(lemma: str) -> str:
    # Raðtölurnar fyrsti og annar beygjast sterkt (skv. wikipedia)
    if lemma == "annar" or lemma == "fyrsti":
        return "s"
    return "v"


def óákveðiðfn(mörk: str) -> bool:
    # Við nýtum skilgreininguna sem er notuð í BÍN, þó listinn sé ekki tæmandi.
    return "SERST" in mörk


def ábfn(lemma: str) -> bool:
    return lemma in {"sá", "þessi", "hinn"}


def óákveðið_ábfn(lemma: str) -> bool:
    return lemma in {"slíkur", "sjálfur", "samur", "sami", "þvílíkur"}


def eignarfn(lemma: str) -> bool:
    return lemma in {"minn", "þinn", "vor", "sinn"}


def spurnarfn(lemma: str) -> bool:
    # "hver", "hvor" og "hvílíkur" get líka verið óákveðin fornöfn.
    return lemma in {"hver", "hvor", "hvaða", "hvílíkur"}


def fn_flokkur(lemma: str, mörk: str) -> str:
    if óákveðiðfn(mörk):
        return "o"
    if ábfn(lemma):
        return "a"
    if óákveðið_ábfn(lemma):
        return "b"
    if eignarfn(lemma):
        return "e"
    if spurnarfn(lemma):
        return "s"
    # Tilvísunarfornöfnin "sem" og "er" eru svo háð samhengi.
    return ""


def parse_bin_str(
    orðmynd: str, lemma: str, kyn_orðflokkur: str, mörk: str
) -> Optional[str]:
    if kyn_orðflokkur == "afn":
        # Afturbeygt fornafn er "fp" en krefst kyns, tölu og falls frumlags í setningu.
        return None
    elif kyn_orðflokkur == "ao":
        return "aa" + stig(mörk)
    elif kyn_orðflokkur == "fn":
        return (
            "f"
            + fn_flokkur(lemma, mörk)
            + kyn(mörk)
            + pers(mörk)
            + tala(mörk)
            + fall(mörk)
        )
    elif kyn_orðflokkur == "fs":
        return "af"
    elif kyn_orðflokkur == "gr":
        return "g" + kyn(mörk) + tala(mörk) + fall(mörk)
    elif kyn_orðflokkur == "hk":
        return "nh" + tala(mörk) + fall(mörk) + greinir(mörk) + sérnafn(orðmynd)
    elif kyn_orðflokkur == "kk":
        return "nk" + tala(mörk) + fall(mörk) + greinir(mörk) + sérnafn(orðmynd)
    elif kyn_orðflokkur == "kvk":
        return "nv" + tala(mörk) + fall(mörk) + greinir(mörk) + sérnafn(orðmynd)
    elif kyn_orðflokkur == "lo":
        return "l" + kyn(mörk) + tala(mörk) + fall(mörk) + beyging(mörk) + stig(mörk)
    elif kyn_orðflokkur == "nhm":
        return "cn"
    elif kyn_orðflokkur == "pfn":
        return "fp" + pfn_kyn(lemma) + pfn_persóna(lemma) + tala(mörk) + fall(mörk)
    elif kyn_orðflokkur == "rt":
        # Raðtölur stigbreytast ekki, svo þær eru alltaf í "frumstigi"
        return "l" + kyn(mörk) + tala(mörk) + fall(mörk) + rt_beyging(lemma) + "f"
    elif kyn_orðflokkur == "so":
        if "SAGNB" in mörk:
            # Sagnbót er túlkað sem lýsingarháttur þátíðar í nefnifall, eintölu, hvorugkyni
            return "sþ" + mynd(mörk) + "hen"
        if "GM-NH-ÞT" == mörk:
            # Tíðin kemur ekki inn.
            return "sng"
        if "GM-BH-ST" == mörk:
            # Stýfður boðháttur.
            return "sbg2en"
        else:
            return (
                "s"
                + háttur(mörk)
                + mynd(mörk)
                + pers(mörk)
                + kyn(mörk)
                + tala(mörk)
                + tíð(mörk)
                + fall(mörk)
            )
    elif kyn_orðflokkur == "st":
        # MÍM markamengið skilgreinir semtengingu og tilvísunarsamtengingu og við getum því ekki greint á milli.
        return None
    elif kyn_orðflokkur == "to":
        # Öll töluorð í BÍN eru frumtölur
        return "tf" + kyn(mörk) + tala(mörk) + fall(mörk)
    elif kyn_orðflokkur == "uh":
        return "au"
    else:
        raise ValueError(f"Unknown {kyn_orðflokkur=}")
