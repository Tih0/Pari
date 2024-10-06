import asyncio, aiofiles
import time
from playwright.async_api import async_playwright, expect

async def reload(iframe):
    button = iframe.locator('div.stream-play-button.flex.cursor-pointer.items-center.bg-w-10.absolute-center')
    button2 = iframe.get_by_text("Подключиться")
    # Проверка на видимость кнопки
    if await button.is_visible() or await button2.is_visible():
        return 1
    else:
        return 0

def extract_after_question_mark(array):
    # Проверяем, есть ли знак вопроса в массиве
    if '?' in array:
        index = array.index('?')  # Находим индекс вопросительного знака
        if index + 1 < len(array):
            return array[index + 1]  # Возвращаем следующий элемент
    return None

async def format_and_save_async(text):
    number = float(text.replace('x', ''))
    async with aiofiles.open('coefficients.txt', 'a') as file:
        await file.write(f"{number}\n")

async def run():
    async with async_playwright() as p:
        # Запускаем браузер
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://hub-web.rupr.upsl-tech.ru/crash-boxing?cid=paribet&lang=ru&productId=crash-boxing")
        await page.wait_for_load_state()
        # try:
        #     button_exit = page.locator('//html/body/application/div[3]/div[2]/svg')
        #     await expect(button_exit).to_be_visible()
        #     await button_exit.click()
        # except:
        #     print("No visitable button_exit")



        selector = 'div.outcome-item-sec.text-w.caption'

        while True:
            if await get_or_wait_for_coefficient(page, selector) == 1:
                await page.reload()


        # button_enter = page.locator('//html/body/application/div[2]/div[1]/div[1]/div/div/div[1]/div/div[2]/span[4]')
        # await button_enter.click()
        # input_login = page.locator('//html/body/application/div[2]/div[1]/div[1]/div/div/div[2]/div/div/form/div/div[2]/div[1]/div[1]/div/input')
        # await input_login.type(login)
        # await asyncio.sleep(4)
        # input_password = page.locator('//html/body/application/div[2]/div[1]/div[1]/div/div/div[2]/div/div/form/div/div[2]/div[2]/div[2]/div[1]/div/input')
        # await input_password.type(password)

async def get_or_wait_for_coefficient(page, selector):
    try:
        iframe = page.frame_locator('iframe[title="sportgamestv-game"]')
        if await reload(iframe):
            return 1
        iframe_element = iframe.locator(selector).first
        current_text = await iframe_element.inner_text()
        if current_text != "?":
            print(current_text, 'kef 1')
            await get_koef2(iframe, selector)

        print("Ожидание изменения знака вопроса на коэффициент...")
        while current_text == "?" or current_text == "-":
            if await reload(iframe):
                return 1
            iframe_element = iframe.locator(selector).first
            current_text = await iframe_element.inner_text()
            await asyncio.sleep(1)
        print(current_text, 'kef 1')
        await format_and_save_async(current_text)
        await get_koef2(iframe, selector)
    except:
        await asyncio.sleep(120)


async def get_koef2(iframe, selector):
    try:
        selector_all_table = "div.outcomes-list.relative.flex.h-100"
        all_table = iframe.locator(selector_all_table)
        all_table_text = await all_table.inner_text()
        lines_array = all_table_text.splitlines()[4::]
        if len(lines_array) == 13:
            index_of_ampersand = (len(lines_array) // 4)
        elif len(lines_array) == 15:
            index_of_ampersand = (len(lines_array) // 4) + 1
        elif len(lines_array) > 15 and len(lines_array) < 17:
            index_of_ampersand = (len(lines_array) // 4) + 3
        elif len(lines_array) == 20:
            index_of_ampersand = (len(lines_array) // 4) + 1
        elif len(lines_array) == 17:
            index_of_ampersand = (len(lines_array) // 4) + 1
        elif len(lines_array) >= 18 and len(lines_array) < 22:
            index_of_ampersand = (len(lines_array) // 4) + 2
        elif len(lines_array) == 22:
            index_of_ampersand = (len(lines_array) // 4) + 1
        elif len(lines_array) == 26:
            index_of_ampersand = (len(lines_array) // 4) + 1
        elif len(lines_array) == 34:
            index_of_ampersand = (len(lines_array) // 4) + 2
        elif len(lines_array) >= 37:
            index_of_ampersand = (len(lines_array) // 4) + 1
            print(lines_array)
            print(f'Len array: {len(lines_array)}')
            print(f'(len(lines_array) // 4): {(len(lines_array) // 4)}')
            print(f"index {index_of_ampersand}")

            iframe_element = iframe.locator(selector).nth(index_of_ampersand)
            current_text = await iframe_element.inner_text()
            print("Ожидание изменения знака вопроса на коэффициент...")
            while current_text != "?":
                if await reload(iframe):
                    return 1
                iframe_element = iframe.locator(selector).nth(index_of_ampersand)
                current_text = await iframe_element.inner_text()
                await asyncio.sleep(2)
            iframe_element = iframe.locator(selector).nth(index_of_ampersand + 1)
            current_text = await iframe_element.inner_text()
            print(current_text, 'kef 2')
            await format_and_save_async(current_text)



        else:
            index_of_ampersand = (len(lines_array) // 4) + 3

        if len(lines_array) < 37:
            print(lines_array)
            print(f'Len array: {len(lines_array)}')
            print(f'(len(lines_array) // 4): {(len(lines_array) // 4)}')
            print(f"index {index_of_ampersand}")

            iframe_element = iframe.locator(selector).first
            current_text = await iframe_element.inner_text()
            print("Ожидание изменения знака вопроса на коэффициент...")
            while current_text != "?":
                if await reload(iframe):
                    return 1
                iframe_element = iframe.locator(selector).first
                current_text = await iframe_element.inner_text()
                await asyncio.sleep(2)
            iframe_element = iframe.locator(selector).nth(index_of_ampersand)
            current_text = await iframe_element.inner_text()
            print(current_text, 'kef 2')
            await format_and_save_async(current_text)
        await asyncio.sleep(10)
    except:
        await asyncio.sleep(120)

# Запускаем асинхронную функцию
asyncio.run(run())
