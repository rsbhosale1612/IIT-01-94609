numbers = input("Enter numbers separated by commas: ")
num_list = [int(n.strip()) for n in numbers.split(",")]

even_count = 0
odd_count = 0

for n in num_list:
    if n % 2 == 0:
        even_count += 1
    else:
        odd_count += 1

print("Total Even Numbers:", even_count)
print("Total Odd Numbers:", odd_count)
