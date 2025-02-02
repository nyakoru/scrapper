def folderVerification(folder_path, report=True):
    """
    folder_path = game folder\n
    report = True for txt file
    report = False for Command Line print
    """
    from command.tools.ArcaneUtils import fetch_json, misc, fetch_file
    errors = []
    warning = []

    from dataclasses import dataclass
    @dataclass
    class Data:
        dictionary:dict
        def ErrorCheck(self, key, message):
            try:
                self.dictionary[key]
            except Exception:
                errors.append(message)

        def WarningCheck(self, key, message):
            try:
                self.dictionary[key]
            except Exception:
                warning.append(message)

    def Notfound(data, key):
        return f"{data} - {key} not found"

    # game_information.json
    game_information = f"{folder_path}/game_information.json"
    if not misc.path_check(game_information):
        errors.append(f"game_information not found")
    else:
        game_information_data = fetch_json(folder_path, "game_information.json").read()
        if game_information_data == {} or game_information_data is None:
            errors.append("No data in game_information.json")
        else:
            data_ = Data(game_information_data)
            data_.ErrorCheck("game"             ,Notfound(game_information_data, "game"))
            data_.ErrorCheck('variant'          ,Notfound(game_information_data, "variant"))
            data_.WarningCheck("game_status"    ,Notfound(game_information_data, "game_status"))
            data_.WarningCheck("variant_status" ,Notfound(game_information_data, "variant_status"))
    errors.append("=====================game_information.json=====================")
    warning.append("=====================game_information.json=====================")

    folders = misc.get_folders(folder_path)    
    for folder in folders:
        # set_information.json
        if not misc.path_check(f"{folder_path}/{folder}/set_information.json"):
            errors.append(f"{folder_path}/{folder} set_information.json not found")
        else:
            set_information = fetch_json(f"{folder_path}/{folder}", "set_information.json").read()
            if set_information == {} or set_information is None:
                errors.append("No data in set_information.json")
            data_ = Data(set_information)
            set_key = f"{folder_path}/{folder}/set_information.json"
            data_.ErrorCheck("setname"          ,Notfound(set_key, "setname"))
            data_.WarningCheck("status"         ,Notfound(set_key, "status"))
            data_.WarningCheck("total"          ,Notfound(set_key, "total"))
            data_.WarningCheck("completed"      ,Notfound(set_key, "completed" ))
            data_.WarningCheck("set_id"         ,Notfound(set_key, "set_id"))
            data_.WarningCheck("variant_id"     ,Notfound(set_key, "variant_id"))
        errors.append(f"====================={folder} set_information.json=====================")
        warning.append(f"====================={folder} set_information.json=====================")
        # single set .json
        if not misc.path_check(f"{folder_path}/{folder}/{folder}.json"):
            errors.append(f"{folder_path}/{folder} {folder}.json not found")
        else:
            cards = fetch_json(f"{folder_path}/{folder}", f"{folder}.json").read()
            for card in cards:
                data_ = Data(card)
                cards_key = f"{folder_path}/{folder}/{folder}.json"
                data_.ErrorCheck("id"           ,Notfound(cards_key, "id"))
                data_.ErrorCheck('name'         ,Notfound(cards_key, 'name'))
                data_.ErrorCheck('product_code' ,Notfound(cards_key, 'product_code'))
                data_.ErrorCheck('rarity'       ,Notfound(cards_key, 'rarity'))
                data_.ErrorCheck('description'  ,Notfound(cards_key, 'description'))
                data_.ErrorCheck('metadata'     ,Notfound(cards_key, 'metadata'))
                data_.WarningCheck("image_id"   ,Notfound(cards_key, "image_id"))
                try:
                    card["product_code"]
                    if not misc.path_check(f"{folder_path}/{folder}/{card["product_code"]}.png"):
                        warning.append(f"No image for {card["name"]} - {card["product_code"]}.png")
                except Exception:
                    pass

        errors.append(f"====================={folder}.json=====================")
        warning.append(f"====================={folder}.json=====================")

    if report is True:
        fetch_file(file_name="Error_Report").writeList(errors)
        fetch_file(file_name="Warning_Report").writeList(warning)
    
    else:
        print("=====================errors=====================")
        for line in errors:
            print(line)
        print("=====================warning=====================")
        for line in warning:
            print(line)
        