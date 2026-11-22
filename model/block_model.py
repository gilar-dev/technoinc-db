from pydantic import BaseModel
from typing import Literal

# GENERAL CONTENT BLOCKS
class GenHeading(BaseModel):
    type: Literal["gen-heading"] = "gen-heading"
    heading: str

class GenSubheading(BaseModel):
    type: Literal["gen-subheading"] = "gen-subheading"
    subheading: str

class GenParagraph(BaseModel):
    type: Literal["gen-paragraph"] = "gen-paragraph"
    text: str

class GenNotes(BaseModel):
    type: Literal["gen-notes"] = "gen-notes"
    text: str

class GenImage(BaseModel):
    type: Literal["gen-image"] = "gen-image"
    src: str
    p_id: str
    desc: str

# INFOBOX CONTENT BLOCKS
class IbStyle(BaseModel):
    type: Literal["ib-style"] = "ib-style"
    b_col: str
    h_col: str
    h_text: str
    sh_col: str
    sh_text: str

class IbHeading(BaseModel):
    type: Literal["ib-heading"] = "ib-heading"
    heading: str

class IbSubheading(BaseModel):
    type: Literal["ib-subheading"] = "ib-subheading"
    subheading: str

class IbText(BaseModel):
    type: Literal["ib-text"] = "ib-text"
    text: str

class IbInfo(BaseModel):
    type: Literal["ib-info"] = "ib-info"
    head: str
    data: str

class IbImage(BaseModel):
    type: Literal["ib-image"] = "ib-image"
    src: str
    p_id: str
    desc: str

# UNIVERSAL CONTENT BLOCKS
class UniRedirect(BaseModel):
    type: Literal["uni-redirect"]
    to: str

# Grouping variety of content blocks
type GeneralBlocks = GenHeading | GenSubheading | GenParagraph | GenNotes | GenImage
type InfoboxBlocks = IbStyle | IbHeading | IbSubheading | IbText | IbInfo | IbImage
type UniversalBlocks = UniRedirect

# Final shape contains variety of content blocks
type Block = GeneralBlocks | InfoboxBlocks | UniversalBlocks