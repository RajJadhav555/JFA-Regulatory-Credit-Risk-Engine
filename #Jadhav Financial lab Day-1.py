#Jadhav Financial lab Day-1
#Author: Raj Dwarkanath Jadhav
#Date:13 October 2026

principal = 100000
rate = 12
time = 3

print("Principal: ", principal)
print("Rate:", rate, "%")
print("Time:", time, "years")

simple_interest = (principal * rate * time) / 100
total_amount = principal + simple_interest

print("Simple Interest: ", simple_interest)
print("Total Amount after ", time, " years: ", total_amount)

compound_amount = principal * (1 + rate / 100) ** time
compound_interest = compound_amount - principal

print("Compound Interest: ", round(compound_interest, 2))
print("Total with compound ", round(compound_amount, 2))
print("Extra earned by Bank:", round(compound_interest - simple_interest, 2))

#EMI calculation

def calculate_emi(P, R, T):
    r = R / (12 * 100)
    n = T * 12
    emi = P * r * (1+r)**n / ((1+r)**n -1)
    return round(emi, 2)

emi = calculate_emi(principal, rate, time)
total_paid = round(emi * time * 12, 2)
interest_paid = round(total_paid - principal, 2)

print("Monthly EMI: ", emi)
print("Total Paid over ", time, " years: ", total_paid)
print("Total Interest Paid: ", interest_paid)