import modal
from pydantic import BaseModel
from enum import Enum


class VehicleColor(str, Enum):
    BEIGE = "Beige"
    BLACK = "Black"
    BROWN = "Brown"
    BURGUNDY = "Burgundy"
    CARBON = "Carbon"
    COPPER = "Copper"
    DARK = "Dark"
    GOLD = "Gold"
    GREY = "Grey"
    NAVY = "Navy"
    PEARL = "Pearl"
    TAN = "Tan"
    UNKNOWN = "Unknown"
    YELLOW = "Yellow"
    BLUE = "Blue"
    GRAY = "Gray"
    GREEN = "Green"
    MAROON = "Maroon"
    ORANGE = "Orange"
    OTHER = "Other"
    PURPLE = "Purple"
    RED = "Red"
    SILVER = "Silver"
    TAN_BROWN = "Tan/Brown"
    WHITE = "White"
    YELLOW_GOLD = "Yellow/Gold"


class Config(BaseModel):
    username: str
    password: str
    firstName: str
    lastName: str
    apartmentNumber: str
    emailAddress: str
    licensePlate: str
    vehicleYear: str
    vehicleMake: str
    vehicleModel: str
    vehicleColor: VehicleColor


app = modal.App(name="moda_dictionary_api")
image = modal.Image.debian_slim(python_version="3.10").pip_install("fastapi[standard]")
moda_configs_dictionary_name = "moda-configs-dictionary"
moda_configs_dict = modal.Dict.from_name(
    moda_configs_dictionary_name, create_if_missing=True
)


@app.function(image=image)
@modal.fastapi_endpoint(method="POST", requires_proxy_auth=True)
async def update_config(config: Config):
    # hmm should there be logic to overwrite existing config?
    # like if a legit user accidentally uses the wrong email it will overwrite
    moda_configs_dict[config.emailAddress] = config
    return "update_config_success"


@app.function(image=image)
@modal.fastapi_endpoint(method="DELETE", requires_proxy_auth=True)
async def delete_config(email: str):
    if email in moda_configs_dict:
        del moda_configs_dict[email]
    return "delete_config_success"


@app.function(image=image)
@modal.fastapi_endpoint(method="GET", requires_proxy_auth=True)
async def list_configs():
    return moda_configs_dict
