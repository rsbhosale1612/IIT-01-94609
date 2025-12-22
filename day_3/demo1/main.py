import calculator
from calculator import multiply
import geomery as geo
import greet

greet.ge("Ranu")

num1 = int(input("Enter num1 : "))
num2 = int(input("Enter num2 : "))

calculator.add(num1, num2)
multiply(num1, num2)


geo.cal_area(num1, num2)
geo.cal_peri(num1, num2)

