import uuid

class GenerateUuid():
    def generate_uuid(self):
        mhi_uuid = uuid.uuid4()
        return str(mhi_uuid)
    
print(GenerateUuid().generate_uuid())