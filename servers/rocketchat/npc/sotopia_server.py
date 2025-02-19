from sotopia.api.fastapi_server import SotopiaFastAPI
import uvicorn

app = SotopiaFastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8800)
