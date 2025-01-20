import json

class PropertiesReader:
    def __init__(self, file_name='config.properties'):
        self.file_name = file_name
        self.properties = {}
        self.read_properties()

    def read_properties(self):
        """Read properties from the file."""
        try:
            with open(self.file_name, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = map(str.strip, line.split('=', 1))
                        
                        # Tentar converter o valor para JSON, caso seja uma string JSON
                        if key == "HEADERS":
                            try:
                                self.properties[key] = json.loads(value)
                            except json.JSONDecodeError:
                                self.properties[key] = value  # Se falhar, manter como string
                        else:
                            self.properties[key] = value
        except FileNotFoundError:
            print(f"File '{self.file_name}' not found. Using empty properties.")
        except Exception as e:
            print(f"Error reading properties: {e}")

    def get_property(self, key, default=None):
        """Retrieve a property by key, with an optional default."""
        return self.properties.get(key, default)

    def set_property(self, key, value):
        """Set or update a property."""
        self.properties[key] = value

    def save_properties(self):
        """Save properties back to the file."""
        try:
            with open(self.file_name, 'w') as file:
                for key, value in self.properties.items():
                    if isinstance(value, dict):  # Converte o dicionário de volta para JSON
                        value = json.dumps(value)
                    file.write(f'{key}={value}\n')
        except Exception as e:
            print(f"Error saving properties: {e}")

    @staticmethod
    def load_properties(file):
        """Load properties from a given file into a dictionary."""
        properties = {}
        try:
            with open(file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = map(str.strip, line.split('=', 1))
                        
                        # Tentar converter o valor para JSON, caso seja uma string JSON
                        if key == "HEADERS":
                            try:
                                properties[key] = json.loads(value)
                            except json.JSONDecodeError:
                                properties[key] = value  # Se falhar, manter como string
                        else:
                            properties[key] = value
        except Exception as e:
            print(f"Error loading properties from file '{file}': {e}")
        return properties

    def __str__(self):
        return str(self.properties)

    def __getitem__(self, key):
        return self.get_property(key)

    def __setitem__(self, key, value):
        self.set_property(key, value)

    def __delitem__(self, key):
        if key in self.properties:
            del self.properties[key]

    def __contains__(self, key):
        return key in self.properties
