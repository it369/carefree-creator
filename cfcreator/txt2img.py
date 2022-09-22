import time

from typing import Any
from fastapi import Response
from cfclient.models import AlgorithmBase

from .common import get_sd
from .common import get_bytes_from_diffusion
from .common import Txt2ImgModel


txt2img_sd_endpoint = "/txt2img/sd"


@AlgorithmBase.register("txt2img.sd")
class Txt2ImgSD(AlgorithmBase):
    endpoint = txt2img_sd_endpoint

    def initialize(self) -> None:
        self.m = get_sd()

    async def run(self, data: Txt2ImgModel, *args: Any) -> Response:
        self.log_endpoint(data)
        t = time.time()
        size = data.w, data.h
        seed = None
        if data.use_seed:
            seed = data.seed
        variation_seed = None
        variation_strength = None
        if data.variation_strength > 0:
            variation_seed = data.variation_seed
            variation_strength = data.variation_strength
        variations = data.variations or None
        self.m.switch_circular(data.use_circular)
        img_arr = self.m.txt2img(
            data.text,
            size=size,
            max_wh=data.max_wh,
            seed=seed,
            variations=variations,
            variation_seed=variation_seed,
            variation_strength=variation_strength,
        ).numpy()[0]
        content = get_bytes_from_diffusion(img_arr)
        self.log_times({"inference": time.time() - t})
        return Response(content=content, media_type="image/png")


__all__ = [
    "txt2img_sd_endpoint",
    "Txt2ImgSD",
]
