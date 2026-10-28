"""Explora un .prproj: para cada MasterClip con nombre dado, lista los VideoClipTrackItem que lo usan y su cadena de componentes."""
import sys; sys.path.insert(0, '.')
from prlib import *

def uses(root, by, name):
    muid = [e.get("ObjectUID") for e in root if e.tag == "MasterClip" and (e.findtext("Name") or "").upper() == name.upper()]
    sub = {e.get("ObjectID"): e for e in root if e.tag == "SubClip" and e.find("MasterClip") is not None and e.find("MasterClip").get("ObjectURef") in muid}
    out = []
    for e in root:
        if e.tag == "VideoClipTrackItem":
            sc = e.find(".//SubClip")
            if sc is not None and sc.get("ObjectRef") in sub:
                comps = []
                chain = e.find(".//ComponentOwner/Components")
                ch = by.get(chain.get("ObjectRef")) if chain is not None else None
                if ch is not None:
                    for c in ch.iter("Component"):
                        r = c.get("ObjectRef")
                        if r in by:
                            comps.append((r, by[r].findtext(".//MatchName"), by[r].findtext(".//Bypass")))
                clip = by[sub[sc.get("ObjectRef")].find("Clip").get("ObjectRef")]
                out.append(dict(item=e.get("ObjectID"), comps=comps, inp=clip.findtext(".//InPoint"), outp=clip.findtext(".//OutPoint"),
                                start=e.findtext(".//TrackItem/Start"), end=e.findtext(".//TrackItem/End"), speed=e.findtext(".//Speed")))
    return out
