import requests
import csv
import matplotlib.pyplot as plt

class App:
    pass

class CovidDataService:
    def __init__(self):
        self.url = "https://covid-api.mmediagroup.fr/v1"
    
    def get_countries_data(self):
        response = requests.get(f"{self.url}/cases")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Error retrieving data from API.")
            return None
    
    def get_countries_historic_data(self):
        response = requests.get(f"{self.url}/history")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Error retrieving data from API.")
            return None

class CSVPlotter:
    def __init__(self):
        pass
    
    def plot_data(self, filename):
        dates = []
        cases = []
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                dates.append(row[0])
                cases.append(int(row[1]))
        plt.plot(dates, cases)
        plt.title('COVID-19 Cases')
        plt.xlabel('Date')
        plt.ylabel('Cases')
        plt.show()

class CSVAdapter(CSVPlotter):
    def __init__(self, covid_data_service):
        super().__init__()
        self.covid_data_service = covid_data_service
    
    def to_csv(self, data):
        with open('covid_data.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Cases'])
            for date, cases in data.items():
                writer.writerow([date, cases])
    
    def plot_data(self):
        data = self.covid_data_service.get_countries_historic_data()
        if data:
            spain_data = data['France']
            spain_cases = {}
            for date, cases in spain_data['All']['dates'].items():
                spain_cases[date] = cases['confirmed']
            self.to_csv(spain_cases)
            super().plot_data('covid_data.csv')

# Prueba
if __name__ == '__main__':
    covid_service = CovidDataService()
    csv_adapter = CSVAdapter(covid_service)
    csv_adapter.plot_data()