from offerup_graphql import OfferUp
from offerup_types import *
import requests
import uuid

EMAIL = "[EMAIL]"
PASSWORD = "[PASSWORD]"

class Listing:
    def __init__(self, api: OfferUp, photos, title, description, price, condition):
        self.api = api
        self.photos = photos
        self.title = title
        self.description = description
        self.price = price
        self.condition = condition
        self.postSession = str(uuid.uuid4())
    
    def post(self):
        try:
            # s3Uuids = list(map(lambda x: S3PhotoUuid(**x), self.api.gql_GeneratePhotoUuids(1)))
            # for uuid in s3Uuids:
            #     requests.put(uuid.location, data=open("./cat.jpeg", 'rb'))
            
            categoryId = self.api.gql_GetAutoCategorization(self.title, self.postSession)['categoryId']
            categoryAttributes = list(map(lambda x: CategoryAttribute(**x), self.api.gql_GetCategoryAttributes(categoryId)))
            requiredCategoryAttributes = [attr.selectValue(0) for attr in categoryAttributes if attr.isRequired()]
            

        except Exception as e:
            print(e)

def login_callback(api:OfferUp):
    listing = Listing(api, None, "Dog", "Dog for sale.", "50", "USED")
    listing.post()


ou = OfferUp(EMAIL, PASSWORD)
ou.login(login_callback)




