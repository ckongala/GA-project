class request_validator:
        
    def validate_data_entries(self, data, expected_keys):
        if not data:
            raise Exception("No data provided, at least one data object is required.")
        
        for i, entry in enumerate(data, start=1):
            missing_keys = [key for key in expected_keys if key not in entry]
            
            if missing_keys:
                missing_key_str = "', '".join(missing_keys)
                raise Exception(f"Please include '{missing_key_str}' in your {i} data entry.")
            
            for key, value in entry.items():
                if not value:
                    raise Exception(f"Missing '{key}' in {i} data entry.")
                
    def validate_data(self, data, expected_keys, is_chunk=False):
        if expected_keys[0] in data:
            if is_chunk and expected_keys[1] in data:
                if data[expected_keys[0]] <= 0:
                    raise Exception(f"Please give a valid '{expected_keys[0]}'")

                if data[expected_keys[1]] == []:
                    raise Exception(f"No data provided in '{expected_keys[1]}' fields.")
            elif not is_chunk:
                if data[expected_keys[0]] == []:
                    raise Exception(f"No data provided in '{expected_keys[0]}', at least one item is required.")
            else:
                raise Exception(f"Missing '{expected_keys[1]}' field in the data for chunk validation.")
        else:
            raise Exception(f"Missing '{expected_keys[0]}' field in the data.")
