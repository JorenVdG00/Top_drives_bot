from app.scraper.scrape_topdrive_records import get_all_info_my_cars
from app.data.db_setup import engine
from app.services.car_service import add_car, get_all_cars, get_all_rids
import requests
import json

def db_scrape_my_cars():
    # Dont forget to clear all cars
    cars_info = get_all_info_my_cars()
    
    for car_info in cars_info.values():
        tune = car_info['tune']
        specs = car_info['info']

        add_car(
            brand=specs['brand'],
            model=specs['onlyName'],
            year=specs['year'], 
            car_class=specs['class'],
            rq=specs['rq'],
            has_abs=specs['abs'],
            has_tcs=specs['tcs'],
            clearance=specs['clearance'],
            tyre=specs['tyres'],
            country=specs['country'],
            drive=specs['drive'],
            fuel=specs['fuel'],
            seats=specs['seats'],
            engine_placement=specs['engine'],
            brake=specs['brake'],
            rid=specs['rid'],
            body_types=specs['bodyTypes'],
            tags=specs['tags'],
            tune=tune)
        
        
        
def scrape_times_all_cars():
    all_rids = get_all_rids()
    print(f"Found {len(all_rids)} cars to scrape")
    
    for index, rid in enumerate(all_rids):
        print(f"Scraping {rid[0]}")
        url = f"https://api.topdrivesrecords.com/car/{rid[0]}"
        response = requests.get(url)
        if response.status_code == 200:
            print(response.text)
            print(f"{index}/{len(all_rids)}:\n  {(response.text)}")
    