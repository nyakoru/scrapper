from command.API_post import APIpost
import time
from command.tools.logrecord import logger
from requests import Response

def process_image_upload(file_path) -> Response:

    def posting_image(image_file):
        logger.info('func posting image')
        files = {"file": image_file}
        response = APIpost('directus_files').post_files(files)
        return response

    logger.info(f"func process_image_upload {file_path}")
    attempts = 0
    max_retries = 3
    while attempts < max_retries:
        try:
            with open(file_path, "rb") as image_file: 
                response:Response = posting_image(image_file)
            if response.status_code == 200 or response.status_code == 201: 
                logger.info('Upload image information success')
                return response
            logger.error(f'PRO-IMG-UPL-{response.status_code} error image upload failed {response.status_code}')
            attempts += 1
            time.sleep(10)
        except Exception as e:
            logger.error(f'PRO-IMG-UPL-{e} image upload process failed')
            attempts += 1
            time.sleep(10)



if __name__ == "__main__":
    file_path = "testimg.jpg"
    response = process_image_upload(file_path=file_path)
    print(response)
