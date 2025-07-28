import uvicorn
from fastapi import FastAPI, Request, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',"Microservices")))
from WorkflowBookGen import Workflow
from JsonifyAndAddHeaders import JsonifyAndAddHeaders
from ConfigReader import ConfigReader
from InternalAPICaller import InternalAPICaller

PortNumber = ConfigReader.get_value("APIEnginesConfig", "APIEngines", "BookGenAPIEngine","PortNumber")
NumberOfWorker = ConfigReader.get_value("APIEnginesConfig", "APIEngines", "BookGenAPIEngine","NumberOfWorker")
Host = ConfigReader.get_value("APIEnginesConfig", "APIEngines", "BookGenAPIEngine","Host")


app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)


app.mount("/dashboard", StaticFiles(directory="static", html=True), name="static")

@app.post("/api/BookGenerate")
async def BookGenerator(request: Request,response: Response):
    try:
        RequestData = await request.json()
        ResponseJson = Workflow.BookGen(RequestData)
        response.status_code = status.HTTP_200_OK

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        ResponseJson = {"Error": f"Book Gen Failed with error {e}."}

    Returnresponse = JsonifyAndAddHeaders.jsonify_and_add_headers(ResponseJson)
    return Returnresponse

@app.get('/api/GetBookIDDetails')
async def GetProcessIDDetail(response: Response,BookID: str = None):
    try:
        ResponseJson = InternalAPICaller.make_request("Get","BookQ","/Queue/GetQData",params={"BookID":BookID})
        response.status_code = status.HTTP_200_OK

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        ResponseJson = {"Error": f"Data Fetch Failed with error {e}."}

    Returnresponse = JsonifyAndAddHeaders.jsonify_and_add_headers(ResponseJson)
    return Returnresponse

@app.get('/api/GetAllBook')
async def GetAllBook(response: Response):
    try:
        ResponseJson = InternalAPICaller.make_request("Get","BookQ","/Queue/GetAllQData")
        response.status_code = status.HTTP_200_OK

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        ResponseJson = {"Error": f"Data Fetch Failed with error {e}."}

    Returnresponse = JsonifyAndAddHeaders.jsonify_and_add_headers(ResponseJson)
    return Returnresponse


@app.get("/api/help")
async def api_info():
    try:
        Guide = {
        "API Guide": {
            "1": {
                "URL": "/Process_NLP_Data",
                "Method": "POST",
                "Payload": "JSON with {'text': 'your input'}",
                "Returns": "ProcessID",
                "Note": "Start NLP processing and get ProcessID"
            },
            "2": {
                "URL": "/Get_ProcessID_Detail",
                "Method": "GET",
                "Params": "ProcessID",
                "Returns": "Result or 'Under Process'",
                "Note": "Poll this to check if result is ready"
            }
        }
    }
        Response = JSONResponse(content=Guide, status_code=200)
    except Exception as e:
        Response = JSONResponse(content=f"Failed with error {e}.", status_code=500)

    return Response


if __name__ == "__main__":
    uvicorn.run("BookGenAPIEngine:app", host=str(Host).strip(), port=int(str(PortNumber).strip()), workers=int(str(NumberOfWorker).strip()))
