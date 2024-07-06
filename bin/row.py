from docxtpl import RichText
from pydantic import BaseModel, field_validator, model_serializer
from typing import Optional
import re
from nums import Nums


FONT = "Times Unicode"

class Row(BaseModel):
    paymanagri_hamar: str
    amsativ: str
    gnord: str
    grancman_hamar: Optional[str]
    hvhh: Optional[str] = None
    andznagir: Optional[str] = None
    trman_amsativ: str
    um_koxmic: str
    grancman_hasce: Optional[str]
    xumb: str
    lot: int
    entalot: Optional[str]
    guyqi_anvanum: str
    meknarkayin_gin: str
    knqman_or: str
    guyqayin_hamar: str
    guyqi_arjeq: str
    voroshman_amsativ: str

    @field_validator('paymanagri_hamar', mode='before')
    @classmethod
    def paymanagri_hamar_validator(cls, v: int) -> str:
        return f"{v:d}"

    @field_validator('hvhh', mode='before')
    @classmethod
    def hvhh_validator(cls, v: int) -> str:
        if v == v:
            return f'ՀՎՀՀ {v:08d},'
        return None

    @field_validator('andznagir', mode='before')
    @classmethod
    def andznagir_validator(cls, v: int) -> str:
        if v == v:
            if re.search(r"\w{2} +\d+", str(v)):
                return f'անձնագիր՝  {v},'
            return f'/Ն/ք՝  {int(v):09d},'
        return None

    @field_validator('um_koxmic', mode='before')
    @classmethod
    def um_koxmic_validator(cls, v: int) -> str:
        return f'{int(v):03d}'

    @field_validator('grancman_hamar', mode='before')
    @classmethod
    def grancman_hamar_validator(cls, v: str) -> str:
        if v == v:
            return f'գրանցման համարը` {v},'
        return None

    @field_validator('xumb', mode='before')
    @classmethod
    def xumb_validator(cls, v: any) -> str:
        if v == v:
            return str(v)
        return None

    @field_validator('entalot', mode='before')
    @classmethod
    def entalot_validator(cls, v: int) -> str:
        if v == v:
            return f'ենթալոտ {v}'
        return None

    @field_validator('lot', mode='before')
    @classmethod
    def lot_validator(cls, v: any) -> int:
        return int(v)

    @field_validator('meknarkayin_gin', 'guyqi_arjeq', mode='before')
    @classmethod
    def gin_validator(cls, v: any) -> str:
        return '{gin}/{gin_bar}/'.format(
            gin='{:,}'.format(int(v)).replace(',', '.'),
            gin_bar=Nums.construct(v)
        )

    @field_validator('guyqayin_hamar', mode='before')
    @classmethod
    def guyqayin_hamar_validator(cls, v: any) -> str:
        guyqayin_hamar = "առանց գույքային համար"
        if re.match(r"\d+", str(v)):
            v = int(v)
            guyqayin_hamar = f'{v:05d}'
        return guyqayin_hamar

    @model_serializer
    def serialize(self):
        return {
            "paymanagri_hamar": RichText(self.paymanagri_hamar, font=FONT, size=14*2, bold=True),
            "amsativ": RichText(self.amsativ, font=FONT, size=10.5*2, underline=True),
            "gnord": RichText(self.gnord, font=FONT, size=10.5*2, bold=True),
            "grancman_hamar": RichText(self.grancman_hamar, font=FONT, size=10.5*2, bold=True),
            "hvhh": RichText(self.hvhh, font=FONT, size=10.5*2, bold=True),
            "andznagir": RichText(self.andznagir, font=FONT, size=10.5*2, bold=True),
            "trman_amsativ": RichText(self.trman_amsativ, font=FONT, size=10.5*2, bold=True),
            "um_koxmic": RichText(self.um_koxmic, font=FONT, size=10.5*2, bold=True),
            "grancman_hasce": RichText(self.grancman_hasce, font=FONT, size=10.5*2, bold=True),
            "xumb": RichText(self.xumb, font=FONT, size=10.5*2, bold=True, underline=True),
            "lot": RichText(self.lot, font=FONT, size=10.5*2, bold=True, underline=True),
            "entalot": RichText(self.entalot, font=FONT, size=12*2, bold=True, underline=True),
            "guyqi_anvanum": RichText(self.guyqi_anvanum, font=FONT, size=12*2, bold=True, underline=True),
            "meknarkayin_gin": RichText(self.meknarkayin_gin, font=FONT, size=12*2, bold=True),
            "knqman_or": RichText(self.knqman_or, font=FONT, size=12*2, bold=True),
            "guyqayin_hamar": RichText(self.guyqayin_hamar, font=FONT, size=12*2, bold=True),
            "guyqi_arjeq": RichText(self.guyqi_arjeq, font=FONT, size=12*2, bold=True),
            "voroshman_amsativ": RichText(self.voroshman_amsativ, font=FONT, size=12*2, bold=False, underline=False),
        }
