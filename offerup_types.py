class S3PhotoUuid:
    def __init__(self, location, uuid):
      self.location = location
      self.uuid = uuid
        

class CategoryAttribute:
    def __init__(self, 
                 attributeName, 
                 merchantRequirement, 
                 consumerRequirement, 
                 priority,
                 values,
                 allowMultipleValues,
                 allowOther,
                 selectionMode):
        self.attributeName = attributeName
        self.merchantRequirement = merchantRequirement
        self.consumerRequirement = consumerRequirement
        self.priority = priority
        self.values = values
        self.allowMultipleValues = allowMultipleValues
        self.allowOther = allowOther
        self.selectionMode = selectionMode
        self.selectedValues = []
    
    def getPossibleValues(self):
        return self.values

    def isMultiSelection(self):
        return True if self.allowMultipleValues == "true" else False

    def selectValue(self, index):
        try:
            if len(self.selectedValues) == 1 and not self.isMultiSelection():
                return
            self.selectedValues.insert(self.values[index])
        except Exception as e:
            print(e)
    
    def isRequired(self):
        return True if self.consumerRequirement == "Required" else False
    
    def __str__(self):
        return str({
            "attributeName": self.attributeName,
            "selectedValues": self.selectedValues
        })

    
class ListingInput:
    def __init__(self,
                 listingId, 
                 postSessionId, 
                 title, 
                 description, 
                 price,
                 isFirmPrice,
                 condition, 
                 categoryId, 
                 categoryAttributes,
                 coverImageSquare,
                 coverImageFullSize,
                 additionalImages,
                 zipcode,
                 shippingEnabled,
                 localPickupEnabled,
                 buyItNowEnabled,
                 isHazardousMaterial,
                 isQrCodeRequested):
        self.listingId = listingId
        self.postSessionId = postSessionId
        self.title = title
        self.description = description
        self.price = price
        self.isFirmPrice = isFirmPrice
        self.condition = condition
        self.categoryId = categoryId
        self.categoryAttributes = categoryAttributes
        self.coverImageSquare = coverImageSquare
        self.coverImageFullSize = coverImageFullSize
        self.additionalImages = additionalImages
        self.zipcode = zipcode
        self.shippingEnabled = shippingEnabled
        self.localPickupEnabled = localPickupEnabled
        self.buyItNowEnabled = buyItNowEnabled
        self.isHazardousMaterial = isHazardousMaterial
        self.isQrCodeRequested = isQrCodeRequested
    
    def pack(self):
        return {
            "postSessionId": self.postSessionId,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "isFirmPrice": self.isFirmPrice,
            "condition": self.condition,
            "categoryId": self.categoryId,
            "categoryAttributes": self.categoryAttributes,
            "coverImageSquare": self.coverImageSquare,
            "coverImageFullSize": self.coverImageFullSize,
            "additionalImages": self.additionalImages,
            "zipcode": self.zipcode,
            "shippingEnabled": self.shippingEnabled,
            "localPickupEnabled": self.localPickupEnabled,
            "buyItNowEnabled": self.buyItNowEnabled,
            "isHazardousMaterial": self.isHazardousMaterial,
            "isQrCodeRequested": self.isQrCodeRequested
        }

        

   

   


  #   "listingInput": {
  #     "listingId": "dd058a6e-d960-36db-ba2c-9a0c2886e907",
  #     "postSessionId": "1743ac8c-4ff9-4166-9db2-aac8ec9eb557",
  #     "title": "Clay",
  #     "description": "Some clay.",
  #     "price": "25",
  #     "isFirmPrice": false,
  #     "condition": "USED",
  #     "categoryId": "2.7",
  #     "categoryAttributes": [
  #       {
  #         "attributeName": "type",
  #         "attributeValue": []
  #       },
  #       {
  #         "attributeName": "brand",
  #         "attributeValue": []
  #       },
  #       {
  #         "attributeName": "material",
  #         "attributeValue": []
  #       }
  #     ],
  #     "coverImageSquare": {
  #       "uuid": "b4bf6c5130324d6f84a42d90783bc709",
  #       "width": 756,
  #       "height": 756
  #     },
  #     "coverImageFullSize": {
  #       "uuid": "238eaa7af2a24f659b9ba5acd30aa8bb",
  #       "width": 756,
  #       "height": 1008
  #     },
  #     "additionalImages": [
  #       {
  #         "uuid": "6c9476859fdc4b24ae10939b0e4ec7bd",
  #         "width": 756,
  #         "height": 1008
  #       },
  #       {
  #         "uuid": "49171f9aa5f940cb989c37a6aadd1c22",
  #         "width": 756,
  #         "height": 1008
  #       }
  #     ],
  #     "latitude": 47.639,
  #     "longitude": -122.356,
  #     "zipcode": "98109",
  #     "shippingEnabled": false,
  #     "localPickupEnabled": true,
  #     "buyItNowEnabled": false,
  #     "isHazardousMaterial": false,
  #     "isQrCodeRequested": false
  #   }
  # },