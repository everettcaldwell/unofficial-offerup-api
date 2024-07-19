from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from gql.client import SyncClientSession


class OfferUp:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.endpoint = "https://client-graphql.offerup.com/"
        self.headers = {
          "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
          "x-ou-d-token": "c46472fefbb905d3",
        }
        self.transport = RequestsHTTPTransport(url=self.endpoint, headers=self.headers)
        self.client = Client(transport=self.transport)
        self.session = SyncClientSession(self.client)
        self.session.connect()
        
    def login(self, login_successful):
        try:
          emailResponse = self.gql_LoginWithEmail()
          if emailResponse['__typename'] == 'MFAOptions':
              mfaResponse = self.gql_LoginWithOTP(emailResponse['phoneOption']['type'])
              if mfaResponse['__typename'] == 'RequestOTPResponse':
                mfaCode = input("2FA Code: ")
                mfaLoginResponse = self.gql_LoginWithEmail(mfaReferenceId=mfaResponse['mfaReferenceId'], mfaCode=mfaCode, challengeId=emailResponse['challengeId'])
                if mfaLoginResponse['__typename'] == 'User':
                   login_successful(self)
              else:
                raise Exception("Unknown MFA response encountered.")
          elif emailResponse['__typename'] == 'User':
              login_successful(self)
          else:
            raise Exception("Unknown response from initial login attempt.")
        except Exception as e:
          print(e)
    def createOrUpdateListing(self, title, description, price, condition, category):
      query = gql(
        """
        
        """
      )
    def refreshInbox(self):
      try:
        alerts = self.gql_GetInboxAlerts()['alerts']
        for alert in alerts:
          print(self.gql_GetChatDiscussion(alert['objectId']))
      except:
        pass
    # gql_GetCategories does not requre session cookie
    def gql_GetCategories(self, zipcode):
      query = gql(
        """
        query GetCategories($input: GetTaxonomyInput) {
          getTaxonomy(input: $input) {
            children {
              id
              currentLevelId
              level
              label
              order
              path
              children {
                id
                currentLevelId
                level
                label
                order
                path
                children {
                  id
                  currentLevelId
                  level
                  label
                  order
                  path
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
        }
        """
      )

      variables = {
        "input": {
          "zipcode": zipcode
        }
      }

      return self.session.execute(document=query, variable_values=variables)['getTaxonomy']
    def gql_LoginWithEmail(self, recaptchaTokenV2=None, recaptchaTokenV3=None, mfaReferenceId=None, mfaCode=None, challengeId=None):
      query = gql(
          """
          mutation LoginWithEmail(
            $email: String!,
            $password: String!,
            $recaptchaTokenV2: String,
            $recaptchaTokenV3: String,
            $mfaReferenceId: ID,
            $mfaCode: String,
            $challengeId: ID
          ) {
            loginWithEmail(
              data: {
                email: $email,
                password: $password,
                recaptchaTokenV2: $recaptchaTokenV2,
                recaptchaTokenV3: $recaptchaTokenV3,
                mfaReferenceId: $mfaReferenceId,
                mfaCode: $mfaCode,
                challengeId: $challengeId
              }
            ) {
              __typename
              ... on User {
                id
                profile {
                  name
                  firstName
                  lastName
                  ratingSummary {
                    average
                    count
                  }
                  avatars {
                    xlImage
                    useDefaultAvatar
                  }
                  dateJoined
                  publicLocationName
                  isAutosDealer
                  isBusinessAccount
                  businessAccountId
                  isTruyouVerified
                  truYouVerificationStatus
                  isPhoneNumberVerified
                  isEmailVerified
                  phoneNumber
                  isSubPrimeDealer
                  followers
                  following
                }
                account {
                  email
                  facebookId
                  isTermsAccepted
                  isPremium
                }
                sessionToken {
                  value
                }
                refreshToken {
                  value
                }
                djangoToken {
                  value
                }
              }
              ... on MFAOptions {
                phoneOption {
                  type
                  redactedDisplayText
                }
                emailOption {
                  type
                  redactedDisplayText
                }
                challengeId
              }
            }
          }
          """
      )
      variables = {
          "email": self.email,
          "password": self.password,
          "recaptchaTokenV2": recaptchaTokenV2,
          "recaptchaTokenV3": recaptchaTokenV3,
          "mfaReferenceId": mfaReferenceId,
          "mfaCode": mfaCode,
          "challengeId": challengeId
      }
      return self.session.execute(document=query, variable_values=variables)['loginWithEmail']
    def gql_LoginWithOTP(self, mfaType):
        query = gql(
          """
          mutation RequestLoginOTP(
            $email: String!,
            $password: String!,
            $mfaType: MfaType!
          ) {
            requestLoginOTP(
              data: {
                email: $email,
                password: $password,
                mfaType: $mfaType
              }
            ) {
              mfaReferenceId
              mfaType
              __typename
            }
          }
          """
        )
        variables = {
          "email": self.email,
          "password": self.password,
          "mfaType": mfaType,
        }
        return self.session.execute(document=query, variable_values=variables)['requestLoginOTP']
    def gql_GetInboxAlerts(self):
        query = gql(
          """
          query GetInboxAlerts($input: InboxAlertsInput!) {
            inboxAlerts(input: $input) {
              alerts {
                ...chatAlert
              }
            }
          }

          fragment chatAlert on Alert {
            id
            actionPath
            contentThumbnails
            dateAdded
            displayAvatar
            eventMetadata
            notificationSource
            notificationText
            objectId
            pinned
            read
            seen
            sender {
              id
              profile {
                avatars {
                  squareImage
                  __typename
                }
                firstName
                isAutosDealer
                isBusinessAccount
                isPremium
                isTruyouVerified
                notActive
                __typename
              }
              __typename
            }
            title
            type
            visualTags {
              displayText
              tag
              type
              __typename
            }
            listingId
            __typename
          }
          """
        )
        variables = {
          "input": {
            "type": "INBOX"
          },
        }
        return self.session.execute(document=query, variable_values=variables)['inboxAlerts']
    def gql_GetChatDiscussion(self, discussionid):
        query = gql(
          """
          query GetChatDiscussion($discussionId: String!, $before: String) {
            discussion(data: {discussionId: $discussionId, before: $before}) {
              itemId
              listingId
              sellerId
              buyerId
              deactivatedUserId
              dateCreated
              lastPostDate
              readStatus {
                userId
                lastReadDate
                __typename
              }
              visualTags {
                tag
                type
                displayText
                __typename
              }
              suggestedMessages {
                id
                text
                __typename
              }
              messages {
                id
                recipientId
                senderId
                text
                sendDateString
                metadataType
                metadata {
                  photos {
                    small {
                      url
                      width
                      height
                      __typename
                    }
                    medium {
                      url
                      width
                      height
                      __typename
                    }
                    large {
                      url
                      width
                      height
                      __typename
                    }
                    __typename
                  }
                  messageUrl
                  systemMessageContext {
                    iconUrl
                    actions {
                      actionPath
                      externalURL
                      actionText
                      __typename
                    }
                    titleText
                    bodyText
                    __typename
                  }
                  place {
                    name
                    formattedAddress
                    placeId
                    longitude
                    latitude
                    __typename
                  }
                  messageButtonText
                  messageTitle
                  __typename
                }
                reaction
                __typename
              }
              listing {
                id
                listingId
                title
                price
                state
                originalPrice
                isFirmOnPrice
                listingCategory {
                  categoryV2 {
                    id
                    l1Id
                    l1Name
                    l2Id
                    l2Name
                    l3Id
                    l3Name
                    name
                    __typename
                  }
                  categoryAttributeMap {
                    attributeName
                    attributePriority
                    attributeUILabel
                    attributeValue
                    attributeValueSource
                    __typename
                  }
                  __typename
                }
                locationDetails {
                  locationName
                  longitude
                  latitude
                  distance
                  city
                  state
                  zipcode
                  __typename
                }
                category {
                  id
                  name
                  levelOneName
                  levelTwoName
                  levelThreeName
                  __typename
                }
                photos {
                  uuid
                  squareSmall {
                    url
                    width
                    height
                    __typename
                  }
                  square {
                    url
                    width
                    height
                    __typename
                  }
                  detailSquare {
                    url
                    width
                    height
                    __typename
                  }
                  small {
                    url
                    width
                    height
                    __typename
                  }
                  detail {
                    url
                    width
                    height
                    __typename
                  }
                  list {
                    url
                    width
                    height
                    __typename
                  }
                  __typename
                }
                fulfillmentDetails {
                  buyItNowEnabled
                  shippingEnabled
                  localPickupEnabled
                  shippingPrice
                  estimatedDeliveryDateStart
                  estimatedDeliveryDateEnd
                  sellerPaysShipping
                  shippingParcelId
                  canShipToBuyer
                  __typename
                }
                __typename
              }
              otherUserRelationship {
                following
                blocked
                __typename
              }
              alertId
              pinned
              availableReactions
              __typename
            }
          }
          """
        )
        variables = {
           "discussionId": discussionid
        }
        return self.session.execute(document=query, variable_values=variables)['discussion']
    def gql_Account(self):
      query = gql(
        """
        query Account {
          me {
            id
            profile {
              name
              firstName
              ratingSummary {
                average
                count
                __typename
              }
              avatars {
                xlImage
                squareImage
                useDefaultAvatar
                __typename
              }
              dateJoined
              publicLocationName
              location {
                name
                publicName
                verified
                __typename
              }
              isAutosDealer
              isBusinessAccount
              businessAccountId
              isTruyouVerified
              truYouVerificationStatus
              isPhoneNumberVerified
              isEmailVerified
              phoneNumber
              isSubPrimeDealer
              followers
              following
              __typename
            }
            account {
              email
              facebookId
              isTermsAccepted
              isPremium
              isPremiumFreeTrialAvailable
              __typename
            }
            userCapabilities {
              canAccessBusinessPortal
              __typename
            }
            __typename
          }
        }
        """
      )
      return self.session.execute(document=query)['me']
    def gql_PublicProfile(self, userId):
      query = gql(
        """
        query PublicProfile($userId: Int, $vanityUserId: ID) {
          publicProfile(userId: $userId, vanityUserId: $vanityUserId) {
            userId
            avatars {
              xlImage
              squareImage
              __typename
            }
            isTruyouVerified
            name
            dateJoined
            publicLocationName
            responseTime
            ratingSummary {
              count
              average
              __typename
            }
            itemsSold
            itemsPurchased
            ratingAttributes {
              count
              value
              __typename
            }
            badges {
              label
              icon
              __typename
            }
            bio
            featureAttributes {
              clickToCallEnabled
              __typename
            }
            c2cPhoneNumber {
              countryCode
              nationalNumber
              __typename
            }
            isAutosDealer
            isBusinessAccount
            isSubPrimeDealer
            isTruyouVerified
            isPremium
            websiteLink
            publicLocation {
              formattedAddress
              name
              latitude
              longitude
              __typename
            }
            openingHours {
              day
              hours
              __typename
            }
            reviews {
              average
              attributionIcon
              googleReviewsReadMoreUrl
              title
              userReviews {
                text
                profilePhotoUrl
                __typename
              }
              __typename
            }
            notActive
            followers
            following
            isFollowedByMe
            lastActive
            __typename
          }
        }
        """
      )
      variables = {
        "userId": userId
      }
      return self.session.execute(document=query, variable_values=variables)['publicProfile']
    def gql_GetAblyConfig(self):
      query = gql(
        """
        query GetAblyConfig {
          channel {
            keyName
            ttl
            timestamp
            capability
            clientId
            nonce
            mac
            __typename
          }
        }
        """
      )
      return self.session.execute(document=query)['channel']
    def gql_UpdateReadDate(self, lastPostDate, discussionId, userId):
      # discussionId provided by alerts query and discussion query
      # lastPostDate is a field provided by discussion query
      # userId = me

      query = gql(
        """
        mutation UpdateReadDate($lastPostDate: String!, $discussionId: String!, $userId: ID!) {
          updateReadDate(
            data: {discussionId: $discussionId, lastPostDate: $lastPostDate, userId: $userId}
          )
        }
        """
      )

      variables = {
        "lastPostDate": lastPostDate,
        "discussionId": discussionId,
        "userId": userId
      }
      return self.session.execute(document=query, variable_values=variables)
    def gql_SendMessage(self, text, discussionId):
      query = gql(
        """
        mutation SendMessage($text: String, $discussionId: String!, $photoUuids: [String!]) {
          postMessage(
            data: {discussionId: $discussionId, text: $text}
            photoUuids: $photoUuids
          )
        }
        """
      )

      variables = {
        "text": text,
        "discussionId": discussionId
      }
      
      return self.session.execute(document=query, variable_values=variables)
    def gql_GeneratePhotoUuids(self, numberOfPhotos):
      query = gql(
        """
        mutation GeneratePhotoUuids($numberOfPhotos: Int!) {
          generateS3PhotoUuids(numberOfPhotos: $numberOfPhotos) {
            location
            uuid
          }
        }
        """
      )
      
      variables = {
        "numberOfPhotos": numberOfPhotos
      }
      
      print
      return self.session.execute(document=query, variable_values=variables)['generateS3PhotoUuids']
    def gql_EvaluateV2(self, categoryId):
      # purchaseState == DEFAULT_FREE
      query = gql(
        """
        query EvaluateV2($categoryId: ID!, $listingId: ID, $summary: Boolean, $zipcode: String) {
          evaluatePurchasePost(
            inputData: {categoryId: $categoryId, listingId: $listingId, summary: $summary, zipcode: $zipcode}
          ) {
            paywallUIVersions
            purchaseState
            overview {
              icon
              tag {
                text
                altText
                tagType
                __typename
              }
              description {
                link {
                  text
                  href
                  linkType
                  __typename
                }
                text
                altText
                __typename
              }
              upsell {
                iconUrl
                link {
                  text
                  href
                  linkType
                  __typename
                }
                description
                iconName
                text
                __typename
              }
              __typename
            }
            purchaseOptions {
              selected
              preferred
              title {
                primary
                secondary
                __typename
              }
              decorator
              decoratorType
              subtitle
              priceToDisplay
              productInfo {
                type
                iconUrl
                link {
                  text
                  href
                  linkType
                  __typename
                }
                paymentDataIos {
                  sku
                  __typename
                }
                paymentDataAndroid {
                  sku
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
        }

        """
      )
      variables = {
        "categoryId": categoryId
      }
      return self.session.execute(document=query, variable_values=variables)['evaluatePurchasePost']
    def gql_GetAutoCategorization(self, title, postSessionId):
      #postSessionId is UUID; example = 1743ac8c-4ff9-4166-9db2-aac8ec9eb557
      query = gql(
        """
        query GetAutoCategorization($title: String!, $postSessionId: String!) {
          autoCategorizeListing(title: $title, postSessionId: $postSessionId) {
            categoryId
            action
            categoryAttributeMap {
              attributeName
              attributeValue
              __typename
            }
            __typename
          }
        }
        """
      )

      variables = {
        "title": title,
        "postSessionId": postSessionId
      }
      return self.session.execute(document=query, variable_values=variables)['autoCategorizeListing']
    
    def gql_GetCategoryAttributes(self, categoryId):
        query = gql(
          """
          query GetCategoryAttributes($categoryId: ID!) {
            getCategoryAttributes(id: $categoryId) {
              attributes {
                attributeName
                merchantRequirement
                consumerRequirement
                priority
                values
                allowMultipleValues
                allowOther
                selectionMode
              }
            }
          }
          """
        )
        variables = {
           "categoryId": categoryId
        }
        return self.session.execute(document=query, variable_values=variables)['getCategoryAttributes']['attributes']

        # "attributes": [
        # {
        #   "attributeName": "brand",
        #   "uiAttributeName": "Brand",
        #   "merchantRequirement": "Required",
        #   "consumerRequirement": "Recommended",
        #   "priority": 1,
        #   "values": null,
        #   "allowMultipleValues": false,
        #   "allowOther": true,
        #   "selectionMode": "SimpleList",
        #   "__typename": "CategoryAttribute"
        # },
      # FORMAT FOR ATTRIBUTES ARGUMENT IN LISTING MUTATION
      #   "categoryAttributes": [
      #   {
      #     "attributeName": "type",
      #     "attributeValue": []
      #   },
      #   {
      #     "attributeName": "brand",
      #     "attributeValue": []
      #   },
      #   {
      #     "attributeName": "material",
      #     "attributeValue": []
      #   }
      # ]

    def gql_GetShippability(self, title, categoryId, zipcode, postSessionId):
      query = gql(
        """
        query GetShippability($title: String!, $categoryId: ID!, $description: String, $latitude: String!, $longitude: String!, $zipcode: String, $postSessionId: String!) {
          shippability(
            title: $title
            categoryId: $categoryId
            description: $description
            latitude: $latitude
            longitude: $longitude
            zipcode: $zipcode
            postSessionId: $postSessionId
          ) {
            allowShipping
            shippingDisabledReason {
              title
              body
              __typename
            }
            shippingEnabledByDefault
            allowBuyNow
            __typename
          }
        }
        """
      )
      variables = {
         "categoryId": categoryId,
         "zipcode": zipcode,
         "postSessionId": postSessionId
      }
      return self.session.execute(document=query, variable_values=variables)['getCategoryAttributes']
     


# Image object format
# {
#         "uuid": "238eaa7af2a24f659b9ba5acd30aa8bb",
#         "width": 756,
#         "height": 1008
# }
    def gql_CreateUpdateListingMutation(self, 
                                        postSessionId, 
                                        title, 
                                        description, 
                                        price, 
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
      query = gql(
        """
        mutation CreateUpdateListingMutation($listingInput: ListingInputV2!) {
          createOrUpdateListingV2(listingInput: $listingInput) {
            title
            originalTitle
            id
            listingId
            conditionText
            description
            price
            listingType
            isFirmOnPrice
            postDate
            postPaymentType
            showPromoPlusUpsell
            fulfillmentDetails {
              shippingEnabled
              buyItNowEnabled
              __typename
            }
            locationDetails {
              locationName
              __typename
            }
            vehicleAttributes {
              vehicleMiles
              __typename
            }
            photos {
              mainImage
              uuid
              list {
                url
                width
                height
                __typename
              }
              __typename
            }
            owner {
              profile {
                isSubPrimeDealer
                isAutosDealer
                isBusinessAccount
                __typename
              }
              __typename
            }
            listingCategory {
              id
              categoryV2 {
                id
                name
                l1Id
                l1Name
                l2Id
                l2Name
                l3Id
                l3Name
                __typename
              }
              categoryAttributeMap {
                attributeName
                attributeValue
                attributePriority
                __typename
              }
              __typename
            }
            __typename
          }
        }
        """
      )
      # cover photo size = 756x756, full foto size = 756x1008 (vertical)
      variables = {
        "listingInput": {
          "postSessionId": postSessionId,
          "title": title,
          "description": description,
          "price": price,
          "condition": condition,
          "categoryId": categoryId,
          "categoryAttributes": categoryAttributes,
          "coverImageSquare": coverImageSquare, # image object
          "coverImageFullSize": coverImageFullSize, 
          "additionalImages": additionalImages, # list image objests
          "zipcode": zipcode,
          "shippingEnabled": shippingEnabled,
          "localPickupEnabled": localPickupEnabled,
          "buyItNowEnabled": buyItNowEnabled,
          "isHazardousMaterial": isHazardousMaterial,
          "isQrCodeRequested": isQrCodeRequested
        }
      }
      return self.session.execute(document=query, variable_values=variables)['createOrUpdateListingV2']



   



#sellerPerformanceSummary

  # "variables": {
  #   "input": {
  #     "fromDate": "2024-03-25",
  #     "toDate": "2024-04-23"
  #   }

# query SellerPerformanceSummary($input: SellerPerformanceSummaryInput) {
#   sellerPerformanceSummary(input: $input) {
#     listingViews {
#       ...performanceSummary
#       __typename
#     }
#     listingsPosted {
#       ...performanceSummary
#       __typename
#     }
#     engagements {
#       ...performanceSummary
#       __typename
#     }
#     listingsSold {
#       ...performanceSummary
#       __typename
#     }
#     __typename
#   }
# }

# fragment performanceSummary on SellerPerformanceSummaryMetric {
#   lastUpdatedTimestamp
#   total
#   __typename
# }

#____

#FetchMyListingsData

# "variables": {
#     "nextPageCursor": "",
#     "limit": 20,
#     "sellFasterSimplificationVariant": "subs_1d_3d",
#     "filters": [
#       {
#         "key": "query",
#         "value": ""
#       }
#     ]
#   },

#_______
# GetUserContext
# "variables": {
#     "input": {
#       "viewportSize": {
#         "width": 411.42857142857144,
#         "height": 840
#       }
#     }
#   },

# query GetUserContext($input: UserContextInput) {
#   userContext(input: $input) {
#     userContext {
#       key
#       value
#       __typename
#     }
#     __typename
#   }
# }

# {
#   "data": {
#     "userContext": {
#       "userContext": [
#         {
#           "key": "device_id",
#           "value": "c46475fefbb805d3",
#           "__typename": "UserContextItem"
#         },
#         {
#           "key": "user_agent",
#           "value": "OfferUp/4.126.0 (build: 412600002; google sdk_gphone64_arm64 UE1A.230829.036.A2; Android 14; en_US)",
#           "__typename": "UserContextItem"
#         },
#         {
#           "key": "app_version",
#           "value": "4.126.0",
#           "__typename": "UserContextItem"
#         },
#         {
#           "key": "device_platform",
#           "value": "android",
#           "__typename": "UserContextItem"
#         },
#         {
#           "key": "user_id",
#           "value": "38934901",
#           "__typename": "UserContextItem"
#         },
#         {
#           "key": "profile_city",
#           "value": "Seattle",
#           "__typename": "UserContextItem"
#         },
#         {
#           "key": "profile_state",
#           "value": "WA",
#           "__typename": "UserContextItem"
#         },
#         {
#           "key": "device.last_known_location.dma_id",
#           "value": "807",
#           "__typename": "UserContextItem"
#         },
#         {
#           "key": "device.last_known_location.dma_name",
#           "value": "San Francisco-Oakland-San Jose, CA",
#           "__typename": "UserContextItem"
#         },
#         {
#           "key": "viewport.width_key",
#           "value": "Med",
#           "__typename": "UserContextItem"
#         },
#         {
#           "key": "viewport.height_key",
#           "value": "Sm",
#           "__typename": "UserContextItem"
#         }
#       ],
#       "__typename": "UserContextResponse"
#     }
#   }
# }

#______
#GetCategories
# "variables": {
#     "input": {
#       "zipcode": "98005"
#     }
#   },

# query GetCategories($input: GetTaxonomyInput) {
#   getTaxonomy(input: $input) {
#     children {
#       id
#       currentLevelId
#       level
#       label
#       order
#       path
#       children {
#         id
#         currentLevelId
#         level
#         label
#         order
#         path
#         children {
#           id
#           currentLevelId
#           level
#           label
#           order
#           path
#           __typename
#         }
#         __typename
#       }
#       __typename
#     }
#     __typename
#   }
# }

# {
#   "operationName": "GetItemDetailDataByItemId",
#   "variables": {
#     "isLoggedIn": true,
#     "deviceLocation": {
#       "latitude": 47.6150436,
#       "longitude": -122.1717577
#     },
#     "itemId": 1686635793
#   },
#   "query": "query GetItemDetailDataByItemId($itemId: Int!, $isLoggedIn: Boolean = false, $deviceLocation: DeviceLocation) {\n  listing(itemId: $itemId, deviceLocation: $deviceLocation) {\n    ...ItemDetailData\n    __typename\n  }\n}\n\nfragment ListingData on Listing {\n  id\n  listingId\n  additionalDetails {\n    key\n    value\n    __typename\n  }\n  availabilityConfirmedAt\n  condition\n  conditionDisplayText\n  description\n  details {\n    key\n    value\n    __typename\n  }\n  fulfillmentDetails {\n    buyItNowEnabled\n    canShipToBuyer\n    isFreeShipping\n    localPickupEnabled\n    shippingEnabled\n    shippingPrice\n    shippingType\n    showBuyNow\n    __typename\n  }\n  isLocal\n  isAutosPost\n  isSold\n  isUnlisted\n  isRemoved\n  lastEdited\n  listingCategory {\n    id\n    categoryAttributeMap {\n      attributeName\n      attributeUILabel\n      attributeValue\n      __typename\n    }\n    categoryV2 {\n      id\n      l1Name\n      l2Name\n      __typename\n    }\n    __typename\n  }\n  locationDetails {\n    latitude\n    locationName\n    longitude\n    __typename\n  }\n  originalPrice\n  owner {\n    id\n    profile {\n      avatars {\n        squareImage\n        __typename\n      }\n      businessInfo {\n        openingHours {\n          day\n          hours\n          __typename\n        }\n        publicLocation {\n          formattedAddress\n          __typename\n        }\n        __typename\n      }\n      clickToCallEnabled\n      dateJoined\n      isAutosDealer\n      isBusinessAccount\n      isSubPrimeDealer\n      isTruyouVerified\n      lastActive\n      name\n      notActive\n      ratingSummary {\n        average\n        count\n        __typename\n      }\n      reviews {\n        average\n        __typename\n      }\n      sellerType\n      websiteLink\n      __typename\n    }\n    __typename\n  }\n  ownerId\n  photos {\n    uuid\n    detailFull {\n      url\n      width\n      height\n      __typename\n    }\n    detailSquare {\n      uuid\n      height\n      url\n      width\n      __typename\n    }\n    __typename\n  }\n  postDate\n  price\n  saved @include(if: $isLoggedIn)\n  title\n  vehicleAttributes {\n    vehicleCityMpg\n    vehicleEpaCity\n    vehicleEpaHighway\n    vehicleExternalHistoryReport {\n      epochDate\n      imageUrl\n      issues\n      price {\n        microUnits\n        __typename\n      }\n      providerName\n      reportUrl\n      __typename\n    }\n    vehicleFundamentals\n    vehicleHighwayMpg\n    vehicleMake\n    vehicleMiles\n    vehicleModel\n    vehicleVin\n    vehicleYear\n    __typename\n  }\n  __typename\n}\n\nfragment ItemDetailData on Listing {\n  ...ListingData\n  formattedOriginalPrice\n  formattedPrice\n  isOwnItem\n  priceDropPercentage\n  showOriginalPrice\n  __typename\n}\n"
# }

