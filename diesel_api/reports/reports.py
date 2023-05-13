from fpdf import FPDF


user =User.query.filter_by(username=username).first_or_404()
trip_cost= 

class PDF_Cost_Report():
    '''
    Creates a PDF file that contains data about the cost of user' trip, 
    who using diesel car.
    '''

    def __init__(self, filename):
        self.filename = filename

    def generate(self, user, trip_cost):
        # user_pay= user.pays(trip_cost)
        pass





    
