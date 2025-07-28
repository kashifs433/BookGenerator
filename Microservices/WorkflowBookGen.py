import os, sys, json, threading, random

microservice_dir = os.path.abspath(os.path.dirname(__file__))
if microservice_dir not in sys.path:
    sys.path.append(microservice_dir)

from InternalAPICaller import InternalAPICaller
from BookIDGenerator import BoookIDGenerator
from LlamaBookGen import GenerativeBookGen
from LlamaResponseCleaner import ResponseCleaner

class Workflow():
    @staticmethod
    def BookGen(RequestData):
        try:
            Book_Type = RequestData.get("Book_Type", "")
            Book_Description = RequestData.get("Book_Description", "")
            Book_Chapter_count = str(random.randint(1, 8)).strip()

            if not Book_Type:
                return JSONResponse(content={"Error": "Book_Type is required"}, status_code=400)
            if not Book_Description:
                return JSONResponse(content={"Error": "Book_Description is required"}, status_code=400)

            #Generating BookID and Adding BookID In Queue
            BookID = BoookIDGenerator.generate_id()
            InternalAPICaller.make_request("POST", "BookQ", "/Queue/InsertDataInQ",payload={"BookID": BookID})
            RequestData["BookID"] = str(BookID)


            #Thread Defination
            def ProcessData(BookID,Book_Type,Book_Description,Book_Chapter_count):
                try:
                    #Generating Book Using Llama
                    Llama_Response = GenerativeBookGen.BookGen(Book_Type,Book_Description,Book_Chapter_count)

                    #Cleaning the Llama Response
                    Clean_Response = json.loads(ResponseCleaner.Extract_Clean_Json(Llama_Response))

                    #Adding Old Data
                    Clean_Response["BookID"] = BookID
                    Clean_Response["Book_Type"] = Book_Type
                    Clean_Response["Book_Description"] = Book_Description
                    Clean_Response["Book_Chapter_count"] = Book_Chapter_count
                    Clean_Response["BookStatus"] = "Book Generation Complete"

                    #Updating Queue
                    InternalAPICaller.make_request("POST", "BookQ", "/Queue/UpdateQData",payload=Clean_Response)

                    return Clean_Response

                except Exception as e:
                    Payload_Data = {"BookID": BookID,
                                    "BookName": "",
                                    "BookStatus":"Error",
                                    "Book_Type":Book_Type,
                                    "Book_Description":Book_Description,
                                    "Book_Chapter_count":Book_Chapter_count,
                                    "Chapters":"",
                                    "Text_Description_Book_Cover_Image":""}
                    InternalAPICaller.make_request("POST", "BookQ", "/Queue/UpdateQData",payload=Payload_Data)
                    return e

            #Starting the Thread
            ThreadProcess_Thread = threading.Thread(target=ProcessData, args=(BookID,Book_Type,Book_Description,Book_Chapter_count))
            ThreadProcess_Thread.start()

            return {"BookID": BookID}

        except Exception as e:
            return e



