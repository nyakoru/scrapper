import asyncio
from command.tools.ArcaneUtils import misc
from dataclasses import dataclass
from typing import Callable
from asyncio import Task

@dataclass
class SeriousHandler:
    ticket_creation: Callable
    download_func: Callable
    set_key: str
    name_key: str
    url_key: str
    multipleinformation: bool = False
    folder_path: str = "sets"
    check: bool = True
    base_url: str = ''
    max_workers: int = 2
    counter = 0
    """
    ticket_creation is a function that needs to return          \n   
        [   1. file name of json file,                          \n
            2. folder_path of where to save file is located,    \n
            3. url link  ]

    base_url : f'{self.base_url}{url}' example https://example.com
    """
    counter +=1
    async def queue_job(self, dict_element, queue):
        """
        If information returns a list of items, multipleinformation == True\n
        If information returns a single item, multipleinformation == False \n
        example of single item: {"file_name":file_name, "folder_path":folder_path, "url":url}
        """

        information = await self.ticket_creation(dict_element, 
                                                   self.set_key, 
                                                   self.name_key, 
                                                   self.url_key, 
                                                   self.folder_path, 
                                                   self.check) #function returns [file_name, folder_path, url]
        if self.multipleinformation:
            for item in information: await queue.put(item)
        else:
            if information: await queue.put(information)

    async def assist_task(self, information:list, semaphore):
        async with semaphore:
            file_name =     information[0]
            folder_path =   information[1]
            downloadfunc = self.download_func(folder_path,False) #directory e.g. ./sets/setname #################
            url =           information[2]

            if url == ("" or None):
                print(f"Downloading blank file: {file_name}")
                await asyncio.to_thread(downloadfunc.blank, url, file_name) #downloads regardless of link availability
                #print(f'blank downloaded {information[1]} {file_name}')
            else:
                full_url = f'{self.base_url}{url}'
                print(f"Downloading image: {full_url}")
                success = await asyncio.to_thread(downloadfunc.image, full_url, file_name)
                if not success: print(f"CMD-ASD-SVC-Failed to download image from {full_url}")

    async def monitor_queue(self, queue):
        while True:
            print(f"Queue size: {queue.qsize()}")
            await asyncio.sleep(1)

    async def main(self, dict_list):
        queue = asyncio.Queue()
        semaphore = asyncio.Semaphore(self.max_workers)
        queue_monitor = asyncio.create_task(self.monitor_queue(queue))

        async def staff():
            while True:
                information = await queue.get()
                if information is None: break
                await self.assist_task(information, semaphore)
                queue.task_done()
        
        service_counter = asyncio.create_task(staff())
        """queue_list = [
            asyncio.create_task(self.queue_job(dict_element, queue))
            for dict_element in dict_list
        ]"""
        for dict_element in dict_list:
            await asyncio.create_task(self.queue_job(dict_element, queue))
            #await asyncio.sleep(0.01)

        #await asyncio.gather(*queue_list)
        await queue.put(None)
        await service_counter


if __name__ == "__main__":
    dict_list = [
        {"name": "image1", "hyperlink": "https://example.com/image1.jpg"},
        {"name": "image2", "hyperlink": "https://example.com/image2.jpg"},
        # Add more dictionary elements as needed
    ]
    #dict sort takes in dict_list, followed by 5 additional settings
    
    #example
    base_url = ""
    processor = SeriousHandler(misc.dict_sort, 
                                   download(directory="images"), 
                                   'card_set', 
                                   'id', 
                                   'imageurl', 
                                   False, 
                                   'test set', 
                                   False, 
                                   base_url, 
                                   max_workers=20)
    asyncio.run(processor.main(dict_list))
