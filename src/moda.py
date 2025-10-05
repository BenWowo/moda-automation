import modal
from pydantic import BaseModel
from enum import Enum
from playwright.async_api import Page
import functools
from datetime import datetime


def log_request(func):
    """
    Decorator to log request details for Modal webhook functions.
    Logs function name, timestamp, request parameters, and response status.
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Get function name
        func_name = func.__name__

        timestamp = datetime.now().isoformat()
        # Log request start

        print(f"START [{timestamp}] {func_name}")

        # Log request parameters
        if args:
            for i, arg in enumerate(args):
                print(f"REQUEST [{func_name}] Arg {i}: {arg}")

        if kwargs:
            for key, value in kwargs.items():
                print(f"REQUEST [{func_name}] {key}: {value}")

        try:
            # Execute the original function
            result = await func(*args, **kwargs)
            print(f"RESPONSE [{func_name}] {result}")
            return result

        except Exception as e:
            # Log any errors
            print(f"ERROR [{func_name}] {str(e)}")
            print(f"ERROR [{func_name}] Exception type: {type(e).__name__}")
            raise  # Re-raise the exception

    return wrapper


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


app = modal.App(name="moda-automation")
image = (
    modal.Image.debian_slim(python_version="3.10")
    .run_commands(
        "apt-get update",
        "apt-get install -y software-properties-common",
        "apt-add-repository non-free",
        "apt-add-repository contrib",
        "pip install playwright==1.42.0",
        "playwright install-deps chromium",
        "playwright install chromium",
    )
    .pip_install("fastapi[standard]")
)
moda_configs_dictionary_name = "moda-configs-dictionary"
moda_configs_dict = modal.Dict.from_name(
    moda_configs_dictionary_name, create_if_missing=True
)


@app.function(image=image)
@modal.fastapi_endpoint(method="POST", requires_proxy_auth=False)
async def update_config(config: Config):
    print(f"config: {config}")
    moda_configs_dict[config.emailAddress] = config
    return "update_config_success"


@app.function(image=image)
@modal.fastapi_endpoint(method="DELETE", requires_proxy_auth=False)
async def delete_config(email: str):
    print(f"email: {email}")
    if email in moda_configs_dict:
        del moda_configs_dict[email]
    return "delete_config_success"


@app.function(image=image)
@modal.fastapi_endpoint(method="GET", requires_proxy_auth=False)
async def list_configs():
    return moda_configs_dict


@app.function(
    image=image,
    schedule=modal.Cron("0 2 * * * ", timezone="America/Chicago"),
)
def get_moda_permits():
    moda_configs = modal.Dict.from_name(
        moda_configs_dictionary_name, create_if_missing=True
    )
    print(f"moda_configs: {moda_configs}")
    print(f"moda_configs.values(): {moda_configs.values()}")
    list(get_moda_permit.map(moda_configs.values()))


@app.function(image=image)
@modal.fastapi_endpoint(method="POST", requires_proxy_auth=False)
async def get_moda_permit_webhook(config: Config):
    print(f"config: {config}")
    await get_moda_permit.local(config)
    return {
        "status": "success",
        "message": f"Permit creation initiated for {config.emailAddress}",
    }


@app.function(image=image)
async def get_moda_permit(config: Config):
    print(f"config: {config}")
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        print(f"Attempting to fill form for [{config.firstName},{config.lastName}]")
        SECOND = 1000
        browser = await p.chromium.launch(
            timeout=30 * SECOND,
        )
        page = await browser.new_page()
        await page.goto("https://tactical.omadi.com/user", wait_until="networkidle")

        await login(page, config)
        print("Logged in")

        await click_register_my_vehicle(page)
        print("Navigated to vehicle registration page")

        await fill_permit_form(page, config)
        print("Filled out vehicle registration form")

        await submit_form(page)
        print("Submitted vehicle registration form")

        await browser.close()
        print("Browser closed.")


async def login(page: Page, config: Config):
    await page.fill("#edit-name", config.username)
    await page.fill("#edit-pass", config.password)
    await page.click("#edit-submit")
    await page.wait_for_load_state("networkidle")


async def click_register_my_vehicle(page: Page):
    await page.click("a[href='https://tactical.omadi.com/permit/new']")
    await page.wait_for_load_state("networkidle")


async def fill_permit_form(page: Page, config: Config):
    first_name_selector = 'input[name="name_0[0][value]"]'
    last_name_selector = 'input[name="cfc_text_0[0][value]"]'
    apartment_number_selector = 'input[name="apartment_number[0][value]"]'
    email_selector = 'input[name="cfc_email_1[0][email]"]'
    license_plate_selector = 'input[name="license_plate[0][plate]"]'
    vehicle_year_selector = 'input[name="vehicle_year[0][value]"]'
    vehicle_make_selector = 'input[name="vehicle[0][make]"]'
    vehicle_model_selector = 'input[name="vehicle[0][model]"]'
    vehicle_color_dropdown_selector = 'div[name="vehicle_color[0][tid]"]'

    await page.fill(first_name_selector, config.firstName)
    await page.fill(last_name_selector, config.lastName)
    await page.fill(apartment_number_selector, config.apartmentNumber)
    await page.fill(email_selector, config.emailAddress)
    await page.fill(license_plate_selector, config.licensePlate)
    await page.fill(vehicle_year_selector, config.vehicleYear)
    await page.fill(vehicle_make_selector, config.vehicleMake)
    await page.fill(vehicle_model_selector, config.vehicleModel)

    await page.click(vehicle_color_dropdown_selector)

    color_map = {
        "Beige": 1,
        "Black": 2,
        "Brown": 3,
        "Burgundy": 4,
        "Carbon": 5,
        "Copper": 6,
        "Dark": 7,
        "Gold": 8,
        "Grey": 9,
        "Navy": 10,
        "Pearl": 11,
        "Tan": 12,
        "Unknown": 13,
        "Yellow": 14,
        "Blue": 15,
        "Gray": 16,
        "Green": 17,
        "Maroon": 18,
        "Orange": 19,
        "Other": 20,
        "Purple": 21,
        "Red": 22,
        "Silver": 23,
        "Tan/Brown": 24,
        "White": 25,
        "Yellow/Gold": 26,
    }

    for _ in range(color_map.get(config.vehicleColor, 0) + 1):
        await page.keyboard.press("ArrowDown")
    await page.keyboard.press("Enter")


async def submit_form(page: Page):
    create_permit_button_selector = 'input[type="submit"][value="Save"]'
    await page.wait_for_selector(create_permit_button_selector, state="visible")
    await page.click(create_permit_button_selector)
    await page.wait_for_load_state("networkidle")


@app.local_entrypoint()
def main():
    get_moda_permits.remote()
