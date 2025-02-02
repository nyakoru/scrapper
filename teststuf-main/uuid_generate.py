import hashlib
import uuid
from dataclasses import dataclass

@dataclass
class UniqID:
    game: str
    variant: str
    set_name:str = ""
    name: str = ""
    product_code: str = ""
    rarity: str = ""
    
    def generate_id(self, set_name:str = "", name:str = "", product_code:str = "", rarity:str = ""):
        """
        Generate a unique identifier based on the attributes of the object.
        :param name: Name of the item
        :param product_code: Product code of the item
        :param rarity: Rarity of the item
        :return: A string representation of a UUID
        """
        self.set_name       = set_name if set_name is not None else ""
        self.name           = name if name is not None else ""
        self.product_code   = product_code if product_code is not None else ""
        self.rarity         = rarity if rarity is not None else ""

        # Combine the attributes into a single string
        data = str(self.combine_())

        # Hash the combined data using SHA-256
        hash_bytes = hashlib.sha256(data.encode(errors='ignore')).digest()

        # Take the first 16 bytes of the hash
        reduced_hash = hashlib.md5(hash_bytes).digest()

        # Create a UUID from the truncated hash
        uuid_obj = uuid.UUID(bytes=reduced_hash, version=4)

        return str(uuid_obj)

    def combine_(self):
        """
        Combine the attributes into a single string for hashing.
        :return: A string combining all attributes
        """
        return (str(self.game), str(self.variant), str(self.set_name), str(self.name), str(self.product_code), str(self.rarity))
    
def imgHash_(image_path:str) -> str:
    """
    Input is the image file location.
    """
    with open(image_path, "rb") as file:
        file_data = file.read()  # Read the image as binary
        md5_hash = hashlib.md5(file_data).digest()  # Generate MD5 hash
        uuid_obj = uuid.UUID(bytes=md5_hash, version=4)
        return str(uuid_obj)