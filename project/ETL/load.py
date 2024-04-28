class Loader:
    def __init__(self):
        pass
    def load_data_and_save(self, input_file, output_path):
        input_file.to_csv(output_path, index = False)
        return True

