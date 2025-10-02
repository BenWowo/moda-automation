import modal
from playwright.async_api import Page
from typing import Dict

ConfigValue = Dict[str, str]
app = modal.App(name="moda-automation")
playwright_image = modal.Image.debian_slim(python_version="3.10").run_commands(
    "apt-get update",
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    "pip install playwright==1.42.0",
    "playwright install-deps chromium",
    "playwright install chromium",
)
moda_configs_dictionary_name = "moda-configs-dictionary"


@app.function(image=playwright_image, schedule=modal.Period(days=1))
def get_moda_permits():
    moda_configs = modal.Dict.from_name(
        moda_configs_dictionary_name, create_if_missing=True
    )
    list(get_moda_permit.map(moda_configs.values()))


@app.function(image=playwright_image)
async def get_moda_permit(config: ConfigValue):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        print(
            f"Attempting to fill form for {config.get('firstName', 'None')} {config.get('lastName', 'None')}"
        )
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


async def login(page: Page, config: ConfigValue):
    await page.fill("#edit-name", config["username"])
    await page.fill("#edit-pass", config["password"])
    await page.click("#edit-submit")
    await page.wait_for_load_state("networkidle")


async def click_register_my_vehicle(page: Page):
    await page.click("a[href='https://tactical.omadi.com/permit/new']")
    await page.wait_for_load_state("networkidle")


async def fill_permit_form(page: Page, config: ConfigValue):
    first_name_selector = 'input[name="name_0[0][value]"]'
    last_name_selector = 'input[name="cfc_text_0[0][value]"]'
    apartment_number_selector = 'input[name="apartment_number[0][value]"]'
    email_selector = 'input[name="cfc_email_1[0][email]"]'
    license_plate_selector = 'input[name="license_plate[0][plate]"]'
    vehicle_year_selector = 'input[name="vehicle_year[0][value]"]'
    vehicle_make_selector = 'input[name="vehicle[0][make]"]'
    vehicle_model_selector = 'input[name="vehicle[0][model]"]'
    vehicle_color_dropdown_selector = 'div[name="vehicle_color[0][tid]"]'

    await page.fill(first_name_selector, config["firstName"])
    await page.fill(last_name_selector, config["lastName"])
    await page.fill(apartment_number_selector, config["apartmentNumber"])
    await page.fill(email_selector, config["emailAddress"])
    await page.fill(license_plate_selector, config["licensePlate"])
    await page.fill(vehicle_year_selector, config["vehicleYear"])
    await page.fill(vehicle_make_selector, config["vehicleMake"])
    await page.fill(vehicle_model_selector, config["vehicleModel"])

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

    for _ in range(color_map.get(config["vehicleColor"], 0)):
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


# another feature would be to collect the
# cookies it gets from signing up and send
# the user an email with a link that gives
# them cookies so they can view the tactical.omadi
# permit
