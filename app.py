import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle

# 3. Create App
app = FastAPI()

# 4. Configure CORS to access API from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello World'}

# 6. Run App
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')

# 7a. Using GET Method
@app.get("/predictStrength")
def getPredictStrength(cement: int, blast_furnace_slag: int, fly_ash: int,water:int,superplasticizer:int,coarse_aggregate:int,fine_aggregate:int,age:int):
    rgModel = pickle.load(open("Gbreg.pkl", "rb"))
    
    prediction = rgModel.predict([[cement,blast_furnace_slag,fly_ash,water,superplasticizer,coarse_aggregate,fine_aggregate,age]])
    
    return {
        'Strength': prediction[0]
    }

# 7b. Using POST Method
from pydantic import BaseModel

class concrete(BaseModel):
    cement: int
    blast_furnace_slag: int
    fly_ash: int
    water:int
    superplasticizer:int
    coarse_aggregate:int
    fine_aggregate:int
    age:int 

@app.post("/predict")
def predictHouseStrength(data: concrete):
    rgModel = pickle.load(open("Gbreg.pkl", "rb"))

    data = data.dict()
    prediction = rgModel.predict([[data["cement"],data["blast_furnace_slag"],data["fly_ash"],data["water"],data["superplasticizer"],data["coarse_aggregate"],data["fine_aggregate"],data["age"]]])
    
    return {
        'Strength': prediction[0]
    }