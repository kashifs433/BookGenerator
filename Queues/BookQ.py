import uvicorn
from fastapi import FastAPI, Request, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',"Microservices")))
from JsonifyAndAddHeaders import JsonifyAndAddHeaders
from ConfigReader import ConfigReader


PortNumber = ConfigReader.get_value("APIEnginesConfig", "APIEngines", "BookQ","PortNumber")
Host = ConfigReader.get_value("APIEnginesConfig", "APIEngines", "BookQ","Host")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.BookDetailQ = {}
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)


@app.post("/Queue/InsertDataInQ")
async def InsertDataInQ(request: Request,response: Response):
        try:
            try:
                data = await request.json()
            except:
                raise RuntimeError("Proper Json Required")

            BookID = data.get("BookID", "")
            if not BookID:
                return JSONResponse(content={"Error": "BookID is required"}, status_code=400)

            BookJson = {
                "BookID" : str(BookID).strip(),
                "BookName" : "",
                "Book_Description" : "",
                "Book_Type" : "",
                "Text_Description_Book_Cover_Image" : "",
                "BookStatus" : "Under Process",
                "Book_Chapter_count" : "",
                "Chapters" : ""
            }

            request.app.state.BookDetailQ[BookID] = BookJson

            response.status_code = status.HTTP_200_OK
            ResponseJson = BookJson

        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            ResponseJson = {"Error": f"Data Insertion Failed with error {e}."}

        Returnresponse = JsonifyAndAddHeaders.jsonify_and_add_headers(ResponseJson)
        return Returnresponse


@app.post('/Queue/UpdateQData')
async def UpdateQData(request: Request,response: Response):
    try:
        BookJson = await request.json()
        BookID = BookJson.get("BookID", "")
        BookName = BookJson.get("BookName", "")
        BookStatus = BookJson.get("BookStatus", "")
        Book_Description = BookJson.get("Book_Description", "")
        Book_Chapter_count = BookJson.get("Book_Chapter_count", "")
        Book_Type = BookJson.get("Book_Type", "")
        Chapters = BookJson.get("Chapters", "")
        Text_Description_Book_Cover_Image = BookJson.get("Text_Description_Book_Cover_Image", "")



        if not BookID:
            return JSONResponse(content={"Error": "BookID is required"}, status_code=400)
        if not BookStatus:
            return JSONResponse(content={"Error": "BookStatus is required"}, status_code=400)

        try:
            if not Chapters:
                Chapters = request.app.state.BookDetailQ[BookID]["Chapters"]
            request.app.state.BookDetailQ[BookID]["BookID"] = BookID
            request.app.state.BookDetailQ[BookID]["BookName"] = BookName
            request.app.state.BookDetailQ[BookID]["Book_Description"] = Book_Description
            request.app.state.BookDetailQ[BookID]["Book_Chapter_count"] = Book_Chapter_count
            request.app.state.BookDetailQ[BookID]["Book_Type"] = Book_Type
            request.app.state.BookDetailQ[BookID]["Text_Description_Book_Cover_Image"] = Text_Description_Book_Cover_Image
            request.app.state.BookDetailQ[BookID]["BookStatus"] = BookStatus
            request.app.state.BookDetailQ[BookID]["Chapters"] = Chapters

        except:
            raise RuntimeError("BookID Not Found")

        response.status_code = status.HTTP_200_OK
        ResponseJson = request.app.state.BookDetailQ[BookID]

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        ResponseJson = {"Error": f"Data Updation Failed with error {e}."}

    Returnresponse = JsonifyAndAddHeaders.jsonify_and_add_headers(ResponseJson)
    return Returnresponse


@app.get('/Queue/GetQData')
async def GetQData(request: Request, response: Response, BookID : str = None):
    try:
        if not BookID:
            return JSONResponse(content={"Error": "BookID is required"}, status_code=400)

        Book_dict = request.app.state.BookDetailQ

        if BookID not in Book_dict:
            return JSONResponse(content={"Error": "BookID Not Found"}, status_code=404)

        response.status_code = status.HTTP_200_OK
        ResponseJson = Book_dict[BookID]

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        ResponseJson = {"Error": f"Data Fetch Failed with error {e}."}

    Returnresponse = JsonifyAndAddHeaders.jsonify_and_add_headers(ResponseJson)
    return Returnresponse


@app.get('/Queue/GetAllQData')
async def GetAllQData(request: Request,response: Response):
    try:
        ResponseJson = request.app.state.BookDetailQ
        response.status_code = status.HTTP_200_OK

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        ResponseJson = {"Error": f"Data Fetch Failed with error {e}."}

    Returnresponse = JsonifyAndAddHeaders.jsonify_and_add_headers(ResponseJson)
    return Returnresponse


if __name__ == "__main__":
    uvicorn.run("BookQ:app", host=str(Host).strip(), port=int(str(PortNumber).strip()), workers=1)
