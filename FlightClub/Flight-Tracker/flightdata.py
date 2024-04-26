class FlightData:
    def __init__(self, price, departure_date, return_date, target_city, target_code):
        self.price = price
        self.departure_date = departure_date
        self.return_date = return_date
        self.city = target_city
        self.code = target_code

    def return_list(self) -> list:
        return [self.city, self.code, self.departure_date, self.return_date, self.price]

    def print_data(self) -> str:
        return (f"Low price alter!\nOnly ${self.price} to fly from Denver-DEN to {self.city}-{self.code} , "
                f"from {self.departure_date} to {self.return_date}.")
