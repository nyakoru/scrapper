class test:
    def test_function():
        import time
        print('testing function')
        time.sleep(5)
        print("time slept 5")
        return "success"

if __name__ == "__main__":
    result = test.test_function()
    from command.tools.ArcaneUtils import fetch_file
    fetch_file(directory="temp",file_name="result").write(result)