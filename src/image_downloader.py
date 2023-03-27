import asyncio
import aiohttp

# TO DOWNLOAD IMAGES: simply call the function download_images()
# urls = list of urls
# directory = where the images will be stored
# extension = the extension for the image name. example : VOX.jpg or WallStreet.jpg


async def download_images_async(urls, directory, extension):
    async with aiohttp.ClientSession() as session:  # asynchronously requests the image links
        await fetch_all_async(session, urls, directory, extension)


async def fetch_all_async(s, urls, directory, extension):
    tasks = []
    number = 0
    for url in urls:
        if url != 'none':
            task = asyncio.create_task(download_image(directory, s, url, f'{number}{extension}'))
            tasks.append(task)  # creates the tasks that will be executed if there is a waiting time

        number += 1

    await asyncio.gather(*tasks)


async def download_image(download_path, s, url, file_name):
    async with s.get(url) as r:  # requests the content of an image_link
        if r.status != 200:  # flags if the link leads to nowhere
            r.raise_for_status()

        image_content = await r.content.read()  # reads the content of the link
        file_path = download_path + file_name  # provides the designated folder for the image
        try:
            with open(file_path, 'wb') as file:  # opens the folder where the image will be placed
                file.write(image_content)  # write the image AKA saves the image inside the folder
        except Exception:
            return
